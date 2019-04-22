import os
from pathlib import Path
import subprocess
import json
from common import AMQP_client

gen_tree = gen_path = pr_set = {}

with open("config.json") as json_file:
	lst = json.load(json_file)
	gen_tree = lst[0]
	gen_path = lst[1]
	pr_set = lst[2]

		
print(gen_path)
def dfs(task_id, root, data):
	if "title" in root:
		for next_node in root["content"]:
			res = dfs(task_id, next_node, data)
			if res != None:
				break
		if res != None:
			return {"title" : root["title"], "content" : res}
		else:
			return None
	else:
		if root["task_id"] == task_id:
			root.setdefault("data_json", data)
			return root;
		else:
			return None


def get_CMD(task_id):
	adr = gen_path[task_id]      #!!!!!!
	print("adr =", adr)
	ext = Path(adr).suffix
	print("ext =", repr(ext))
	print("pr_set =", repr(pr_set))
	cmd = pr_set[ext]   #!!!!!!
	print("cmd in get_CMD =", cmd)
	cmd = cmd.replace("_FILE", adr)
	return cmd

         

def call_Generator(task_id, args):
	cmd = gen_path[task_id] #!!!!!!!
	if(Path(cmd).exists()):
		try:
			cmd = get_CMD(task_id)
			if args != "":
				cmd = cmd + args
			print("cmd =", cmd)
			p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
			p.wait()
			_data = p.stdout.read()
			return _data
		except:
			return "error: can`t open generator " + task_id 
	else:
		return "error: wrong path to generator: " + cmd
	
def get_args(a):
	args = ""
	for k in a:
		args += " " + str(k) + "=\"" + str(a[k]) + "\""
	return args
				
		                                  
""" MyClient """

class MyClient(AMQP_client):
	
	def process_data(self, Id, _data, task_id):
		if _data == 'error':
				self.send('interface', Id, 'error_post_task', _data)
		else:
			to_base = dfs(task_id, gen_tree, _data)
			print("to_base =", to_base)
			self.send('database', Id, 'save_task', to_base);
			print("_data =", repr(_data))
			_tdata = json.dumps([json.loads(_data)])
			print("_tdata =", repr(_tdata))
			self.send('latex', Id, 'post_task', _tdata);
	
	def post_taskList(self, Id):
		G = json.dumps(gen_tree)
		self.send('interface', Id, 'post_taskList', G)
		   	
	def post_task(self, Id, Type, Data):
		task_id = Data["task_id"]
		print("Data", Data)
		print("task_id",task_id)
		args = get_args(Data["args"])
		if task_id in gen_path.keys():
			_data = call_Generator(task_id, args)
			self.process_data(Id, _data, task_id)
		else:
			self.send('interface', Id, 'error_post_task', 'Task is not in list')	
				
	
	def parse(self, Id, Type, Data):
		if Type == 'get_taskList':
			self.post_taskList(Id)
		else:
			if Type == 'get_task':
				self.post_task(Id, Type, Data)
			else:
				self.send('interface', Id, 'error_post_task', 'Wrong request type')
				

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