from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from collections import deque
import json

from .models import TaskTree, TaskType, Task
import taskgen.communications as comm

# Create your views here.

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
		return render(request, 'taskgen/task_list.html', {'db_list': tree})

def db_list(request):
	db_list = TaskType.objects.all()
	return render(request, 'taskgen/task_list.html', {'db_list': db_list})

def statements(request):
	tasks_id = list(request.POST.keys())[1:]
	tasks = []
	for it in tasks_id:
		tasks.extend(map(lambda x: x.read_file(), Task.objects.filter(task_id__pk=it)))
	print('output =', tasks)
	return render(request, 'taskgen/statements.html', {'tasks': tasks})

def change_task(request):
	return HttpResponse('TODO изменение задачи')