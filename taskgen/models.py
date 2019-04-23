from django.db import models

import json

# Create your models here.



class TaskType(models.Model):

	description = models.CharField('description', max_length=200)

	def __str__(self):
		return self.description


class Task(models.Model):

	task_id = models.ForeignKey(TaskType, on_delete=models.CASCADE)
	data_path = models.FileField('source_json', upload_to='task_storage/')

	def read_file(self):
		with self.data_path.open() as j_fin:
			read_data = j_fin.read()
		return json.loads(read_data)