import pika, pickle, threading

class AMQP_client:
	"""Класс для общения между сервисами"""
	def __init__(self, Host, e_name, e_type="fanout"):
		"""Host - адрес (хост) сервера RabbitMQ
		e_name, e_type - имя и тип точки доступа на которой"""
		self.host = Host
		self.e_name = e_name
		self.e_type = e_type
		self.connection = None
	
	def start_consume(self):
		"""Подключение к RabbitMQ для получения сообщений от других сервисов"""
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.host))
		channel = self.connection.channel()
		channel.exchange_declare(exchange = self.e_name, exchange_type = self.e_type)
		self.q_name = channel.queue_declare('', exclusive=True).method.queue
		channel.queue_bind(exchange = self.e_name, queue = self.q_name)
		channel.basic_consume(queue = self.q_name, on_message_callback = self.callback, auto_ack = True)
		consume_thread = self.ThreadAMQP(channel)
		consume_thread.start()

	def stop_consume(self):
		"""Закрытие подключения"""
		self.connection.close()

	def parse(self, Id, Type, Data):
		"""НЕОБХОДИМА РЕАЛИЗАЦИЯ в конечном сервисе. Обработка поступающих от других сервисов сообщений"""
		pass

	def callback(self, ch, method, properties, body):
		"""Обработчик сообщений от RabbitMQ"""
		received = pickle.loads(body)
		self.parse(received.Id, received.Type, received.Data)

	def send(self, to_name, Id, Type, Data=None, to_type="fanout"):
		"""Отправка сообщений через RabbitMQ другим сервисам"""
		connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.host))
		channel = connection.channel()
		channel.exchange_declare(exchange = to_name, exchange_type = to_type)
		channel.basic_publish(exchange = to_name, routing_key = '', body = pickle.dumps(self.Message(Id, Type, Data)))
		connection.close()

	class ThreadAMQP(threading.Thread):
		"""Запуск прослушки сообщений из RabbitMQ в отдельном потоке"""
		def __init__(self, channel):
			threading.Thread.__init__(self)
			self.channel = channel

		def run(self):
			self.channel.start_consuming()

	class Message:
		"""Класс сообщений, пересылаемых между сервисами"""
		def __init__(self, Id, Type, Data):
			self.Id, self.Type, self.Data = Id, Type, Data
