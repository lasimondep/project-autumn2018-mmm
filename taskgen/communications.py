import time

from common import AMQP_client


_REQUEST_TIMEOUT, _QUEUE_TIMEOUT = 1, 10


class InterfaceClient(AMQP_client):
	class RequestID:
		_ID = 0
		def __next__(self):
			InterfaceClient.RequestID._ID += 1
			return InterfaceClient.RequestID._ID
	request_id = RequestID()

	class TimeOutExcept(Exception):
		pass

	def __init__(self, Host, e_name, e_type='fanout'):
		super(InterfaceClient, self).__init__(Host, e_name, e_type)
		self.ans_queue = list()

	def send_request(self, to_name, Type, Data=None, to_type='fanout'):
		Id = next(InterfaceClient.request_id)
		self.send(to_name, Id, Type, Data, to_type)
		time.sleep(_REQUEST_TIMEOUT)
		if Id not in map(lambda x: x['Id'], self.ans_queue):
			raise InterfaceClient.TimeOutExcept()
		else:
			res = list(filter(lambda x: x['Id'] == Id, self.ans_queue))[0]
			return res['Type'], res['Data']

	def parse(self, Id, Type, Data):
		self.ans_queue = list(filter(lambda x: time.time() - x['time'] < _QUEUE_TIMEOUT, self.ans_queue))
		self.ans_queue.append({'time': time.time(), 'Id': Id, 'Type': Type, 'Data': Data})


interface_client = InterfaceClient("localhost", "interface")
interface_client.start_consume()