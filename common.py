import pika, pickle

class AMQP_client:
	'''класс для общения между сервисами'''
	connection = channel = 0
	def __init__(self, Host, e_name, e_type):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host = Host))
		channel = connection.channel()
		channel.exchange_declare(exchange = e_name, exchange_type = e_type)
		self.q_name = channel.queue_declare('', exclusive=True).method.queue
		channel.queue_bind(exchange = e_name, queue = self.q_name)
		channel.basic_consume(queue = self.q_name, on_message_callback = self.callback, auto_ack = True)
		channel.start_consuming()

	def parse(self, ch, Id, Type, Data):
		pass

	def callback(self, ch, method, properties, body):
		received = pickle.loads(body)
		self.parse(ch, received.Id, received.Type, received.Data)

	def send(self, Channel, to_name, to_type, Id, Type, Data = b''):
		Channel.exchange_declare(exchange = to_name, exchange_type = to_type)
		Channel.basic_publish(exchange = to_name, routing_key = '', body = pickle.dumps(self.Message(Id, Type, Data)))

	class Message:
		'''класс сообщений: Id для получения ответа, Type - строка'''
		def __init__(self, Id, Type, Data):
			self.Id, self.Type, self.Data = Id, Type, Data
