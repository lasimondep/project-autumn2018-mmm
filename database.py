from common import AMQP_Client
import sqlite3


class DatabaseClient(AMQP_Client):
	def parse(self, Id, Type, Data):
		if Type == "save_task":
			add_task(Data)

_DB_NAME = "db_task.sqlite3"

def db_insert(cmd, **kwarg):
	print("db_insert", kwarg)
	connection = sqlite3.connect(_DB_NAME)
	cursor = connection.cursor()
	cursor.execute(cmd, kwarg)
	connection.commit()
	cursor.execute("SELECT last_insert_rowid()")
	rowid = cursor.fetchall()
	connection.close()
	return rowid[0][0]

def db_select(cmd, **kwarg):
	print("db_select", kwarg)
	connection = sqlite3.connect(_DB_NAME)
	cursor = connection.cursor()
	cursor.execute(cmd, kwarg)
	result = cursor.fetchall()
	connection.close()
	return result

def db_update(cmd, **kwarg):
	print("db_update", kwarg)
	connection = sqlite3.connect(_DB_NAME)
	cursor = connection.cursor()
	cursor.execute(cmd, kwarg)
	connection.commit()
	connection.close()

def add_task(raw_ie):
	def exist_fold(parent_id, title):
		if parent_id == None:
			result = db_select("""SELECT tree_id FROM task_tree
								WHERE parent_id IS NULL
								AND title = :title""",
								title=title)
		else:
			result = db_select("""SELECT tree_id FROM task_tree
								WHERE parent_id = :parent_id
								AND title = :title""",
								parent_id=parent_id, title=title)
		if len(result) > 0:
			return True, result[0][0]
		else:
			return False, None

	def add_subfolder(parent_id, title):
		exist, node = exist_fold(parent_id, title)
		if exist:
			return node
		if parent_id == None:
			parent_id = db_insert("""INSERT INTO task_tree (title)
									VALUES (:title)""",
									title=title)
		else:
			parent_id = db_insert("""INSERT INTO task_tree (parent_id, title)
									VALUES (:parent_id, :title)""",
									parent_id=parent_id, title=title)
		return parent_id

	def add_task_type(task_id, parent_id, description):
		db_insert("""INSERT OR IGNORE INTO task_type (task_id, parent_id, description)
					VALUES (:task_id, :parent_id, :description)""",
					task_id=task_id, parent_id=parent_id, description=description)

	it = raw_ie
	parent_id = None
	while "title" in it.keys():
		parent_id = add_subfolder(parent_id, it["title"])
		it = it["content"]

	add_task_type(it["task_id"], parent_id, it["description"])

	inner_id = db_insert("""INSERT INTO tasks (task_id)
							VALUES (:task_id)""",
							task_id=it["task_id"])
	json_source = "./storage/json/t" + str(inner_id) + ".json"
	with open(json_source, "w") as jout:
		json.dump(it["data_json"], jout)
	db_update("""UPDATE tasks
				SET json_source = :json_source
				WHERE inner_id = :inner_id""",
				json_source=json_source, inner_id=inner_id)


Client = DatabaseClient("localhost", "database")
Client.start_consume()
print("Database started consuming")
try:
	while True:
		pass
except KeyboardInterrupt:
	Client.stop_consume()
	print("Close connection & stop thread")