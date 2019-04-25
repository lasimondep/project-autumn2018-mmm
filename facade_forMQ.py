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
    	if "task_id" in node.keys():
    		timeouts.setdefault(node["task_id"], node["timeout"])
    	else:
    		for c in node["content"]:
    			d.append(c)
    return timeouts	


with open("config.json", 'rb') as json_file:
	lst = json.load(json_file)
	gen_tree = {'title' : 'root', 'content' : lst[0]}
	gen_path = lst[1]
	pr_set = lst[2]
	timeouts = bfs(gen_tree)

def get_CMD(task_id):
	adr = gen_path[task_id]     
	ext = Path(adr).suffix
	cmd = pr_set[ext]   
	cmd = cmd.replace("_FILE", adr)
	return cmd

         

def call_Generator(task_id, args = None):
	cmd = gen_path[task_id] 
	if(Path(cmd).exists()):
		cmd = get_CMD(task_id)
		if args != None:
			cmd = cmd + args
		try:
			p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			p.wait(timeout = timeouts[task_id])
			_data = p.stdout.read()
			_err = p.stderr.read()
			if _err == b'':
				return _data
			else:
				return None
		except TimeoutExpired:
			p.kill()
			return None
	else:
		return None
	
def get_arg(args, i):
	if args != None:
		arg = ""
		a = args[i]
		for k in a:
			arg += " " + str(k) + "=\"" + str(a[k]) + "\""
		return arg
	else:
		return None

def process_one(Data)
	arg = get_arg(Data["args"])
	task_id  = Data["task_id"]
	_data = call_Generator(task_id, arg)
	return [{"task_id" : task_id, "json" : _data}]
	
def process_data(Data):
	_data = []
	for req in Data:
		task_id = req["task_id"]
		if task_id in gen_path.keys():
			for i in range(req["count"]):
				_from_gen = call_Generator(task_id)
				if _from_gen != None:            #TODO: обработка ошибок???
					_data.append({"task_id": task_id, "json" : _from_gen})	
	return _data
	
		                                  
""" MyClient """

class MyClient(AMQP_client):

	def post_taskList(self, Id):
		self.send('interface', Id, 'post_taskList', gen_tree)
		   	
	def post_task(self, Id, Type, Data):
		_data = self.process_one(Data)
		self.send('latex', Id, 'post_task', _data)
					
	
	def get_task_text(self, Id, Type, Data):
		task_id = Data["task_id"]
		_data = self.process_data(Data)
        self.send('latex', Id, 'post_task_text', _data)	
	
	def parse(self, Id, Type, Data):
		if Type == 'get_taskList':
			self.post_taskList(Id)
		else:
			if Type == 'get_task':
				self.post_task(Id, Type, Data)
			else:
				if Type == 'get_task_text':
					self.get_task_text(Id, Type, Data)
				else:
					self.send('interface', Id, 'error_post', 'Wrong request type')
				

if __name__ == '__main__':
	client = MyClient('localhost', 'facade')
	client.start_consume()
	print("Facade started consuming")
	try:
		while True:
			pass
	except KeyboardInterrupt:
		client.stop_consume()
		print("Close connection & stop thread")