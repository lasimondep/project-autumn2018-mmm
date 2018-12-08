from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection

class GenReqId:
	_ID = 0
	def next():
		GenReqId._ID = GenReqId._ID + 1
		return GenReqId._ID

class Hosts:
	def set_hosts(*hosts):
		Hosts.Interface, Hosts.Facade, Hosts.Tex, Hosts.DataBase = hosts

def get_taskList():
	connection = HTTPConnection(Hosts.Interface)
	reqID = GenReqId.next()
	connection.request("GET", "/", headers={"request": "get_taskList", "reqID": reqID})
	#connection.request("GET", "/list.html") debug only
	response = connection.getresponse()
	connection.close()
	rheaders, rdata = response.getheaders(), response.read()
	return rdata

def get_task_Facade(serverInstance, taskID):
	connection = HTTPConnection(Hosts.Facade)
	reqID = GenReqId.next()
	connection.request("GET", "/", headers={"request": "get_task", "reqID": reqID, "taskID": taskID})
	#connection.request("GET", "/task.json") debug only
	response = connection.getresponse()
	connection.close()
	rheaders, rdata = response.getheaders(), response.read()
	return rdata

def get_Tex(taskID):
	connection = HTTPConnection(Hosts.Tex)
	reqID = GenReqId.next()
	connection.request("GET", "/", headers={"request": "get_Tex", "reqID": reqID})
	#connection.request("GET", "/task.tex") debug only
	response = connection.getresponse()
	connection.close()
	rheaders, rdata = response.getheaders(), response.read()
	return rdata

class MediatorHTTPRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		request, reqID = self.headers["request"], self.headers["reqID"]
		#TODO check Fasade is runing
		if request == "get_taskList":
			taskList = get_taskList(self.server)
			print(taskList)
			self.send_response(200)
			self.send_header("response", "get_taskList")
			self.send_header("resID", reqID)
			self.end_headers()
			self.wfile.write(taskList)
		if request == "get_task":
			taskID = self.headers["taskID"]
			#TODO request from database
			taskFile = get_task_Facade(self.server, taskID)
			texFile = get_Tex(self.server, taskFile)
			send_response(200)
			self.send_header("response", "get_task")
			self.send_header("resID", reqID)
			self.send_header("Content-Type", "text/tex;charset=utf-8")
			self.end_headers()
			self.wfile.write(taskFile)

serv = HTTPServer(("127.0.0.1", 25800), MediatorHTTPRequestHandler)
Hosts.set_hosts(["127.0.0.1", 25500], ["127.0.0.1", 25600], ["127.0.0.1", 25700], ["127.0.0.1", 25900])
serv.serve_forever()