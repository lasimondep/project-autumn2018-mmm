import os
import subprocess
import json
from common import AMQP_client
from setup import gen_set, pr_set

#Generators = {10: Generator(10, 'T10.py', 'Задача №10'), 2 :Generator(2,'TestGen.py', 'Тестовый генератор 2')}


class Generator:
	def __init__(self, t, adr, d, c):
		self.task = t;
		self.ADR = adr
		self.descr = d
		self.cond = c

Generators = {}

for	t in gen_set.keys():
	Generators.setdefault(t, Generator(t, gen_set[t][0], gen_set.get[t][1], gen_set.get[t][2])


def get_CMD(task_id):
	adr = Generators.get(task_id).ADR
	ext = Path(adr).suffix
	cmd = pr_set[ext]
	cmd.replace(_FILE, adr.replace(ext, '')) 	

         
def Gens_Cond():
	data = [];
	for i in Generators.keys():
		nd = {"Task_ID" : Generators.get(i).task, "Description" : Generators.get(i).descr, "Condition" : Generators.get(i).cond }
		data.append(nd)
	return data



def call_Generator(task_id, args):
	cmd = Generstors.get(task_id).ADR
	if(Path(cmd).exists()):
		try:
			cmd = setup.get_CMD(task_id)
			if args != "":
				cmd = cmd + args
			p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
			p.wait()
			_data = p.stdout.read()
			return _data
		except:
			return "error: can`t open generator " + task_id 
	else:
		return "error: wrong path to generator: " + cmd
	
	
		                                  
""" MyClient """

class MyClient(AMQP_client):
	
	def process_data(self, Id, _data):
		if _data == 'error':
				self.send('interface', Id, 'error_post_task', _data) 
				Generators.get(task_id).cond = 'broken'
	
	def post_taskList(self, Id):
		data = Gens_Cond()
		G = json.dumps(data)
		self.send('interface', Id, 'post_taskList', G)
   	
   	def post_task(self, Id, Type, Data):
   		task_id = Data["task_id"]
		args = Data["args"]
		if Generators.get(task_id) != None:
			_data = call_Generator(task_id, args)
			self.process_data(Id, _data)
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
	try:
		while True:
			pass
	except KeyboardInterrupt:
		client.stop_consume()