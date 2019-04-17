from common import AMQP_client

class InterfaceClient(AMQP_client):
	def parse(self, Id, Type, Data):
		if Type == "post_taskList":
			self.send("facade", "fanout", 2, "Thank you")
			print("Task list:", Data)

Client = InterfaceClient("localhost", "interface")
Client.start_consume()
print("At this time must run Django web-server")
Client.send("facade", 1, "get_taskList")
try:
	while True:
		pass
except KeyboardInterrupt:
	Client.stop_consume()
	print("Close connection & stop thread")
