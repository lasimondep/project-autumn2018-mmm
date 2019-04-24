from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

import json

# Create your models here.


class TaskTree(MPTTModel):
	
	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
	description = models.CharField('description', max_length=200)
	task_id = models.CharField('task_id', max_length=200, null=True)

	class MPTTMeta:
		order_insertion_by = ['-level']

class TaskType(MPTTModel):

	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
	description = models.CharField('description', max_length=200)

	class MPTTMeta:
		order_insertion_by = ['-level']

	def __str__(self):
		return self.description


class Task(models.Model):

	task_id = models.ForeignKey(TaskType, on_delete=models.CASCADE)
	data_path = models.FileField('source_json', upload_to='task_storage/')

	def read_file(self):
		with self.data_path.open() as j_fin:
			read_data = j_fin.read()
		return json.loads(read_data)