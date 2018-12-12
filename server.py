from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection
from get_json import get_json_file

class GenReqId:
	_ID = 0
	def next():
		GenReqId._ID = GenReqId._ID + 1
		return GenReqId._ID


def get_request(req, data=None, **addhead):
	connection = HTTPConnection("127.0.0.1:25500")
	reqID = GenReqId.next()
	head = {"request": req, "reqID": reqID}
	head.update(addhead)
	connection.request("GET", '/', headers=head, body=data)
	response = connection.getresponse()
	connection.close()
	return response.getheaders(), response.read()

def get_json(taskFile):
	rheaders, rdata = get_request("get_json", taskFile)
	return rdata

class TexHTTPRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		request, reqID = self.headers["request"], self.headers["reqID"]
		data = self.rfile.read()
		if request == "get_tex":
			self.send_response(200)
			self.send_header("response", "get_tex")
			self.send_header("resID", reqID)
			self.send_header("Content-Type", "text/tex;charset=utf-8")
			self.end_headers()
			self.wfile.write(get_json_file(data))

serv = HTTPServer(("127.0.0.1", 25800), TexHTTPRequestHandler)
serv.serve_forever()
