from common import AMQP_client

class MyClient(AMQP_client):
	def __init__(self, Host, e_name, e_type):
		super().__init__(Host, e_name, e_type)
	
	def parse(self, ch, Id, Type, Data):
		if Type == 'get_taskList':
			self.send(ch, 'interface', 'fanout', 1, 'post_taskList', 'Hello World!')

client = MyClient('localhost', 'facade', 'fanout')