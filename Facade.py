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


Generators = {10: Generator(10, 'T10.py', 'Задача №10'), 2 :Generator(2,'TestGen.py', 'Тестовый генератор 2')}

         
def Gens_Cond():
	data = [];
	for i in Generators.keys():
		nd = {"Task_ID" : Generators.get(i).task, "Description" : Generators.get(i).descr, "Condition" : Generators.get(i).cond }
		data.append(nd)
	return data

""" Request Handler """

class FacadeHandler(BaseHTTPRequestHandler):    
	def do_GET(self):                          
		rootdir = os.getcwd().replace('\\','/')   
		try:   
			if self.headers['request'] == 'get_taskList': #запрос списка задач 
				self.send_response(200)   
				self.send_header('request','get_taskList') 
				self.end_headers()          
				data = Gens_Cond()
				G = json.dumps(data)
				self.wfile.write(G.encode('utf-8'))  
			if self.headers['request'] == 'get_task':                                                                                                 
				id = int(self.headers['taskID'])
				conLen = int(self.headers["Content-Length"])
				bd = self.rfile.read(conLen)
				
				print(bd)
				if Generators.get(id) != None:
					cmd= rootdir + '/' + Generators.get(id).IP
					print(cmd)
					if(Path(cmd).exists()):
						try:
							p = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE)
							p.wait()
							_fin = open("_stdout", "rb")
							_data = _fin.read()     
							data = p.stdout.read()
							self.send_response(200)
							self.send_header('request','get_task')
							self.send_header('task.ID', self.headers['task.ID'])
							self.end_headers()
							self.wfile.write(_data)
						except:
							self.send_error(405)
							Generators.get(id).cond = 'broken'
					else:
						self.send_error(404)
						Generators.get(id).cond = 'broken'
				else:
					print(id);
					print(Generators.get(id))                    
					self.send_error(403)
			else:
				self.send_error(402)              
		except IOError:
			self.send_error(401)
			
def run(server_class=HTTPServer, handler_class=FacadeHandler):
	server_address = ('127.0.0.1', 25500)
	httpd = server_class(server_address, handler_class)
	try:
		print('server is running')
		httpd.serve_forever()
	except KeyboardInterrupt:
		print('server terminated by keyboard')

if __name__ == '__main__':
	run()

		
	