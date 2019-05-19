#!/usr/bin/env python3
import os
from pathlib import Path
import subprocess
import json
from collections import deque
from common import AMQP_client


def bfs(root):
    timeouts = {}
    d = deque()
    d.append(root)
    while d:
        node = d.popleft()
        if 'task_id' in node.keys():
            timeouts.setdefault(node['task_id'], node['timeout'])
        else:
            for c in node['content']:
                d.append(c)
    return timeouts


def get_CMD(task_id):
    adr = gen_path[task_id]
    ext = Path(adr).suffix
    cmd = pr_set[ext]
    cmd = cmd.replace('_FILE', adr)
    return cmd


def call_Generator(task_id, args=None):
    cmd = gen_path[task_id]
    if Path(cmd).exists():
        cmd = get_CMD(task_id)
        if args != None:
            cmd = cmd + args
        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait(timeout = timeouts[task_id])
            _data = p.stdout.read()
            _err = p.stderr.read()
            print(_data)
            print(_err)
            if _err == b'':
                return _data
            else:
                return None
        except TimeoutExpired:
            p.kill()
            return None
    else:
        return None


def get_arg(args):
    if args != None:
        arg = ''
        a = args
        i = 1
        for k in a:
            if k != None:
                arg += ' ' + str(i) + '=\"' + str(k) + '\"'
        return arg
    else:
        return None


def process_one(Data):
    arg = get_arg(Data.get('args'))
    task_id  = Data['task_id']
    _data = call_Generator(task_id, arg)
    if _data == None:
        return []
    return [{'task_id' : task_id, 'json' : _data}]


def process_data(Data):
    _data = []
    for req in Data:
        task_id = req['task_id']
        if task_id in gen_path.keys():
            for i in range(req['count']):
                _from_gen = call_Generator(task_id)
                if _from_gen != None:			#TODO: обработка ошибок???
                    _data.append({'task_id': task_id, 'json' : _from_gen})
    return _data


class MyClient(AMQP_client):
    """ MyClient """
    def post_taskList(self, Id):
        self.send('interface', Id, 'post_taskList', gen_tree)

    def post_task(self, Id, Type, Data):
        _data = process_one(Data)
        if _data != []:
            self.send('latex', Id, 'get_task', _data)

    def get_task_text(self, Id, Type, Data):
        _data = process_data(Data)
        if _data != []:
            self.send('latex', Id, 'get_task_text', _data)

    def parse(self, Id, Type, Data):
        if Type == 'get_taskList':
            self.post_taskList(Id)
        else:
            if Type == 'get_task':
                self.post_task(Id, Type, Data)
            else:
                if Type == 'get_task_text':
                    self.get_task_text(Id, Type, Data)


if __name__ == '__main__':
    with open('config.json', 'rb') as json_file:
        lst = json.load(json_file)
        #gen_tree = {'title' : 'root', 'content' : lst[0]}
        gen_tree = lst[0]
        gen_path = lst[1]
        pr_set = lst[2]
        timeouts = bfs(gen_tree)
    client = MyClient('localhost', 'facade')
    client.start_consume()
    print('Facade started consuming')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        client.stop_consume()
        print('Close connection & stop thread')
