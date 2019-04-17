import os
import re
import subprocess
import json
from pathlib import Path
from common import AMQP_client

""" Файл с настройками запуска генераторов """
GG = open('generators.txt', 'r')
GS = open('gensettings.txt', 'r')
sttngs = {}

for line in GS:
	if line[0] != "#":
		l = line.split(maxsplit = 1)
		sttngs.setdefault( l[0], (l[1])[:-1])	

GS.close()

print(sttngs)

Generators = {}

""" Класс генератор содержит в себе ip процесса-генератора и номер задачи (потом, возможно, список подзадач) """

class Generator:
	def __init__(self, t, ip, d):
		self.task = t;
		self.IP = ip
		self.descr = d
		self.cond = 'works'

for line in GG:
	if line[0] != '#':
		l = line.split(maxsplit = 3)
		Generators.setdefault(l[0], Generator(l[0], l[1], l[2]))

print(Generators)
#Generators = {10: Generator(10, 'T10.py', 'Задача №10'), 2 :Generator(2,'TestGen.py', 'Тестовый генератор 2')}

         
def Gens_Cond():
	data = [];
	for i in Generators.keys():
		nd = {"Task_ID" : Generators.get(i).task, "Description" : Generators.get(i).descr, "Condition" : Generators.get(i).cond }
		data.append(nd)
	return data
	                                  
""" MyClient """

class MyClient(AMQP_client):
	def __init__(self, Host, e_name, e_type):
		super().__init__(Host, e_name, e_type)
	
	def parse(self, ch, Id, Type, Data):
		rootdir = os.getcwd().replace('\\','/')
		if Type == 'get_taskList':
			data = Gens_Cond()
			G = json.dumps(data)
			self.send('interface', 'fanout', 1, 'post_taskList', G)
		else:
			if Type == 'get_task':
				task_id = Data[task_id]
				args = Data[args]
				if Generators.get(task_id) != None:
					cmd = rootdir + '/' + Generators.get(id).IP
					if(Path(cmd).exists()):
						try:
							ext = Path(cmd).suffix
							cmd = sttngs[ext] + " " + cmd
							if args != "":
								cmd = cmd + args
								p = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE)
								p.wait()
								_fin = open('_stdout', 'rb')
								_data = _fin.read()
								if _data == 'error':
									self.send('interface', 'fanout', 1, 'error_post_task', _data)   
								else:
									self.send('latex', 'fanout', 1, 'post_task', _data)
									#self.send(ch, 'database', 'fanout', 1, 'post_task', _data)
						except:
							self.send('interface', 'fanout', 1, 'error_post_task', 'Generator broken') 
							Generators.get(task_id).cond = 'broken'
				    else:
				    	self.send('interface', 'fanout', 1, 'error_post_task', 'Generator`s path invalid. Check the setup file')
				else:
					self.send('interface', 'fanout', 1, 'error_post_task', 'Task is not in list')
			else:
				self.send('interface', 'fanout', 1, 'error_post_task', 'Wrong request type')
				

if __name__ == '__main__':
	client = MyClient('localhost', 'facade', 'fanout')
	try:
		client.start_consume()
	except KeyboardInterrupt:
        client.stop_consume()

