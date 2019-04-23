from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.defaulttags import register

from .models import TaskType, Task

# Create your views here.

@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)

def index(request):
	return render(request, 'taskgen/index.html')

def generate_list(request):
	return HttpResponse('TODO запрос списка задач из фасада')

def db_list(request):
	db_list = TaskType.objects.all()
	return render(request, 'taskgen/db_list.html', {'db_list': db_list})

def load_tasks(request):
	tasks_id = list(request.POST.keys())[1:]
	tasks = []
	for it in tasks_id:
		tasks.extend(map(lambda x: x.read_file(), Task.objects.filter(task_id__pk=it)))
	output = []
	for it in tasks:
		i = 0
		while i < len(it['text']['text1']):
			if i % 2 != 0:
				it["text"]["text1"][i] = str(it["inserts"][it["text"]["text1"][i]])
			i += 1
		output.append(it['text'])
	print('output =', output)
	return render(request, 'taskgen/load.html', {'tasks': output})

def change_task(request):
	return HttpResponse('TODO изменение задачи')