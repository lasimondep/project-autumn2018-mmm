from http.server import BaseHTTPRequestHandler, HTTPServer 
import os
import threading
import re
import subprocess
import json
from pathlib import Path

""" Класс генератор содержит в себе ip процесса-генератора и номер задачи (потом, возможно, список подзадач) """

class Generator:
	def __init__(self, t, ip, d):
		self.task = t;
		self.IP = ip
		self.descr = d
		self.cond = 'works'


Generators = {11: Generator(11, 'TestGen.py', 'Тестовый генератор'), 2 :Generator(2,'TestGen2.py', 'Тестовый генератор 2')}

         
def Gens_Cond():
	data = [];
	for i in Generators.keys():
		nd = {"Task_ID" : Generators.get(i).task, "Description" : Generators.get(i).descr, "Condition" : Generators.get(i).cond }
		data.append(nd)
	return data

""" Request Handler """

class FacadeHandler(BaseHTTPRequestHandler):    
	def do_GET(self):                                          
		rootdir ="C:/Users/Public/Documents/Programming/Project"   
		try:   
			if self.headers['request'] == 'get_tasklist': #запрос списка задач 
				self.send_response(200)   
				self.send_header('request','get_tasklist') 
				self.end_headers()          
				data = Gens_Cond()
				G = json.dumps(data)
				self.wfile.write(G.encode('utf-8'))  
			if self.headers['request'] == 'get_task':                                                                                                 
				id = int(self.headers['taskID'])
				if Generators.get(id) != None:
					cmd=rootdir+'/' + Generators.get(id).IP
					if(Path(cmd).exists()):
						try:
							p = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE)
							p.wait()
							print(cmd)
							self.send_response(200)
							self.send_header('request','get_task')
							self.send_header('task.ID', self.headers['task.ID'])
							self.end_headers()
							self.wfile.write(p.stdout.read())
						except:
							self.send_error(405)
							Generators.get(id).cond = False
					else:
						self.send_error(405)
						Generators.get(id).cond = False
				else:
					print(id);
					print(Generators.get(id))                    
					self.send_error(406)              
		except IOError:  
			self.send_error(404)
			       
def run(server_class=HTTPServer, handler_class=FacadeHandler):
	server_address = ('127.0.0.1', 8000)
	httpd = server_class(server_address, handler_class)
	try:
		print('server is running')
		httpd.serve_forever()
	except KeyboardInterrupt:
		print('server terminated by keyboard')

if __name__ == '__main__':
	run()

		
	