from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

import json

# Create your models here.


class TaskTree(MPTTModel):
	
	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
	description = models.CharField('description', max_length=200)
	task_id = models.CharField('task_id', max_length=200, null=True, blank=True)
	task_timeout = models.FloatField('timeout', null=True, blank=True)

	class MPTTMeta:
		order_insertion_by = ['-level']

	def __str__(self):
		return self.description


class TaskType(MPTTModel):

	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
	description = models.CharField('description', max_length=200)
	task_id = models.CharField('task_id', max_length=200, null=True, blank=True)

	class MPTTMeta:
		order_insertion_by = ['-level']

	def __str__(self):
		return self.description


class Task(models.Model):

	parent = models.ForeignKey(TaskType, on_delete=models.CASCADE)
	data_path = models.FileField('source_json', upload_to='task_storage/', null=True, blank=True)
	data_raw = models.FileField('raw_json', upload_to='task_storage/raw/', null=True, blank=True)
	user = models.ManyToManyField(User, null=True, blank=True)

	def read_raw(self):
		with self.data_raw.open() as j_fin:
			read_data = j_fin.read()
		return json.loads(read_data)

	def read_file(self):
		with self.data_path.open() as j_fin:
			read_data = j_fin.read()
		return json.loads(read_data)

	def save_raw(self, data):
		self.data_raw.save('r' + str(self.pk) + '.json', ContentFile(data))

	def save_file(self, data):
		self.data_path.save('t' + str(self.pk) + '.json', ContentFile(data))