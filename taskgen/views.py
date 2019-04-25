from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaulttags import register
from django.shortcuts import render
from collections import deque
import json
import random

from .models import TaskTree, TaskType, Task
import taskgen.communications as comm

# Create your views here.

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def index(request):
	return render(request, 'taskgen/index.html')

def generate_list(request):
	try:
		Type, Data = comm.interface_client.send_request('facade', 'get_taskList')
	except comm.InterfaceClient.TimeOutExcept:
		return HttpResponse('Фасад временно недоступен')
	else:
		TaskTree.objects.all().delete()
		tree = TaskTree.objects.create(description=Data['title'])
		bfs_queue = deque()
		bfs_queue.append((Data, tree))
		while len(bfs_queue) > 0:
			node, parent = bfs_queue.popleft()
			for it in node['content']:
				if 'title' in it.keys():
					bfs_queue.append((it, TaskTree.objects.create(description=it['title'], parent=parent)))
				else:
					TaskTree.objects.create(description=it['description'], task_id=it['task_id'], parent=parent)
	tree = TaskTree.objects.all()
	return render(request, 'taskgen/task_list.html', {'task_list': tree, 'get_from': 'facade'})

def db_list(request):
	db_list = TaskType.objects.all()
	return render(request, 'taskgen/task_list.html', {'task_list': db_list, 'get_from': 'db'})

statements_output = None

def statements(request):
	get_from = request.POST['get_from']
	global statements_output
	if get_from == 'facade' or get_from == 'db':
		tasks = list(request.POST.keys())[2:]
		tasks = list(filter(lambda x: int(request.POST[x]) > 0, tasks))
		tasks = [(int(x), int(request.POST[x])) for x in tasks]
		statements_output = []
		if get_from == 'db':
			for it in tasks:
				res = list(Task.objects.filter(parent__pk=it[0]))
				random.shuffle(res)
				task_type = TaskType.objects.get(pk=it[0])
				statements_output.append({'task_id': task_type.task_id, 'description': task_type.description, 'tasks': list(map(lambda x: x.read_file(), res[:it[1]]))})
		if get_from == 'facade':
			gen_request = []
			timeout = 0
			for it in tasks:
				res = TaskTree.objects.get(pk=it[0])
				timeout += res.task_timeout * it[1]
				gen_request.append({'task_id': res.task_id, 'count': it[1]})
			print('\ngen_request =', gen_request, '\n')
			try:
				Type, Data = comm.interface_client.send_request('facade', 'get_task', Data=gen_request, timeout=timeout)
			except comm.InterfaceClient.TimeOutExcept:
				return HttpResponse('Фасад временно недоступен')				
#			Data = [{'task_id': 'm2', 'tex': ['Calculate ', '15', ' with ', '24']},
#					{'task_id': 'i1', 'tex': ['Calculate ', '-50', ' with ', '500']},
#					{'task_id': 'i2_2', 'tex': ['Hello ', '30', r' $\frac{1}{2}$ ', '100']}]
			group_tasks = {}
			for it in Data:
				if it['task_id'] in group_tasks.keys():
					group_tasks[it['task_id']].append(it['tex'])
				else:
					group_tasks[it['task_id']] = [it['tex']]
			for it in group_tasks.keys():
				task_type = TaskTree.objects.get(task_id=it)
				statements_output.append({'task_id': task_type.task_id, 'description': task_type.description, 'tasks': group_tasks[it]})

				#Добавление в базу
				try:
					task_type = TaskType.objects.get(task_id=it)
				except TaskType.DoesNotExist:
					task_type = None
				if task_type != None:
					for one_task in group_tasks[it]:
						task_new = Task.objects.create(parent=task_type)
						task_new.save_file(json.dumps(one_task))
				else:
					task_path = list(TaskTree.objects.get(task_id=it).get_ancestors(include_self=True))
					try:
						task_type = TaskType.objects.get(description=task_path[0].description)
					except TaskType.DoesNotExist:
						task_type = TaskType.objects.create(description=task_path[0].description, task_id=task_path[0].task_id)
					for tp in task_path[1:]:
						try:
							task_type = TaskType.objects.filter(parent=task_type).get(description=tp.description)
						except TaskType.DoesNotExist:
							task_type = TaskType.objects.create(parent=task_type, description=tp.description, task_id=tp.task_id)
					for one_task in group_tasks[it]:
						task_new = Task.objects.create(parent=task_type)
						task_new.save_file(json.dumps(one_task))
		return render(request, 'taskgen/statements.html', {'types': statements_output, 'get_from': 'change'})
	if get_from == 'change':
		return render(request, 'taskgen/statements.html', {'types': statements_output, 'get_from': 'change'})

#def change_task(request):
#	return render(request, 'taskgen/debug.html', {'debug': str(type(request.POST['savedata']))})