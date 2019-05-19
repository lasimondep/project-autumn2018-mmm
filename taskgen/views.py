from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaulttags import register
from django.shortcuts import render
from django.urls import reverse
from collections import deque
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

import json, random, os, pylatex

from .models import TaskTree, TaskType, Task
import taskgen.communications as comm

# Create your views here.


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def login_view(request):
    if 'login-button' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            error_msg = 'Ошибка в имени пользователя и(или) пароле'
            return render(request, 'taskgen/login.html', {'error_msg': error_msg})
        else:
            login(request, user)
            return HttpResponseRedirect(reverse('taskgen:index'))
    else:
        return render(request, 'taskgen/login.html')


def register_view(request):
    if 'register-button' in request.POST:
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            user_check = 'Пользователь уже существует'
            return render(request, 'taskgen/register.html', {'user_check':user_check})
        username = request.POST['username']
        password = request.POST['password']
        print(password, username)
        user = User.objects.create_user(username, None, password)
        user.save()
        print(user)
        return HttpResponseRedirect(reverse('taskgen:index'))
    else:
        return render(request, 'taskgen/register.html')


def index(request):
    if 'logout-button' in request.POST:
        logout(request)
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
                    TaskTree.objects.create(description=it['description'], task_id=it['task_id'], parent=parent, task_timeout=it['timeout'])
    tree = TaskTree.objects.all()
    return render(request, 'taskgen/task_list.html', {'task_list': tree, 'get_from': 'facade'})


def db_list(request):
    db_list = TaskType.objects.all()
    return render(request, 'taskgen/task_list.html', {'task_list': db_list, 'get_from': 'db'})


def debug_statements(request):
    request.session.setdefault('rand', random.random())
    return render(request, 'taskgen/debug.html', {'debug': str(request.session.items())})



def statements(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('taskgen:index'))
    get_from = request.POST['get_from']
    if get_from == 'facade' or get_from == 'db':
        tasks = list(request.POST.keys())[2:]
        if 'hide_watched' in request.POST.keys():
            tasks = tasks[1:]
        tasks = list(filter(lambda x: int(request.POST[x]) > 0, tasks))
        tasks = [(int(x), int(request.POST[x])) for x in tasks]
        statements_output = request.session['statements'] = []
        statements_nraw = request.session['statements_raw'] = []
        if get_from == 'db':
            for it in tasks:
                queryset = Task.objects.filter(
                    parent__pk=it[0],
                )
                if 'hide_watched' in request.POST.keys():
                    queryset = queryset.exclude(
                        user__username=request.user
                    )
                res = list(queryset)
                random.shuffle(res)
                task_type = TaskType.objects.get(pk=it[0])
                if request.user.is_authenticated:
                    currentuser = User.objects.get(username=request.user)
                    for itt in res[:it[1]]:
                        itt.user.add(currentuser)
                        itt.save()
                statements_output.append({'task_id': task_type.task_id, 'description': task_type.description, 'tasks': list(map(lambda x: x.read_file(), res[:it[1]]))})
                statements_nraw.append(list(map(lambda x: x.read_raw(), res[:it[1]])))

        if get_from == 'facade':
            gen_request = []
            timeout = 0
            for it in tasks:
                res = TaskTree.objects.get(pk=it[0])
                timeout += res.task_timeout * it[1]
                gen_request.append({'task_id': res.task_id, 'count': it[1]})
            print('\ngen_request =', gen_request, '\n')
            try:
                Type, Data = comm.interface_client.send_request('facade', 'get_task_text', Data=gen_request, timeout=timeout)
            except comm.InterfaceClient.TimeOutExcept:
                return HttpResponse('Фасад временно недоступен')
            group_tasks = {}
            for it in Data:
                if it['task_id'] in group_tasks.keys():
                    group_tasks[it['task_id']].append({'text': json.loads(it['json']), 'raw': json.loads(it['raw'])})
                else:
                    group_tasks[it['task_id']] = [{'text': json.loads(it['json']), 'raw': json.loads(it['raw'])}]
            for it in group_tasks.keys():
                task_type = TaskTree.objects.get(task_id=it)
                statements_output.append({'task_id': task_type.task_id, 'description': task_type.description,
                                          'tasks': list(map(lambda x: x['text'], group_tasks[it]))})
                statements_nraw.append(list(map(lambda x: x['raw'], group_tasks[it])))

                #Добавление в базу
                try:
                    task_type = TaskType.objects.get(task_id=it)
                except TaskType.DoesNotExist:
                    task_type = None
                if task_type != None:
                    for one_task in group_tasks[it]:
                        task_new = Task.objects.create(parent=task_type)
                        if request.user.is_authenticated:
                            currentuser = User.objects.get(username=request.user)
                            task_new.user.add(currentuser)
                            task_new.save()
                        task_new.save_file(json.dumps(one_task['text']))
                        task_new.save_raw(json.dumps(one_task['raw']))
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
                        task_new.save_file(json.dumps(one_task['text']))
                        task_new.save_raw(json.dumps(one_task['raw']))
        return render(request, 'taskgen/statements.html', {'types': statements_output, 'get_from': 'change'})
    if get_from == 'change':
        POST_dict = dict(request.POST)
        statements_output = request.session['statements']
        statements_nraw = request.session['statements_raw']
        selected_task = str(list(filter(lambda x: x.startswith('button'), POST_dict.keys()))[0])[6:]
        selected_type, selected_num = map(lambda x: int(x) - 1, selected_task.split('.'))
        task_id = statements_output[selected_type]['task_id']
        changed_list = POST_dict.get('checkbox' + selected_task, [])
        insert_list = POST_dict.get('insert' + selected_task, [])
        changed_list = list(map(lambda x: int(x) // 2, changed_list))
        gen_request = []
        it = 1
        while it <= len(insert_list):
            if it in changed_list:
                gen_request.append(insert_list[it - 1])
            else:
                gen_request.append(None)
            it += 1
        if gen_request == []:
            gen_request = {'task_id': task_id}
        else:
            gen_request = {'task_id': task_id, 'args': gen_request}
        try:
            Type, Data = comm.interface_client.send_request('facade', 'get_task', Data=gen_request, timeout=2)
        except comm.InterfaceClient.TimeOutExcept:
            statements_output[selected_type]['tasks'][selected_num] = ['Генератор для данной задачи временно недоступен']
        else:
            statements_output[selected_type]['tasks'][selected_num] = json.loads(Data[0]['json'])
            statements_nraw[selected_type][selected_num] = json.loads(Data[0]['raw'])
        return render(request, 'taskgen/statements.html', {'types': statements_output, 'get_from': 'change'})


def download(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('taskgen:index'))
    statements_input = request.session['statements_raw']
    doc_request = []
    for it in statements_input:
        doc_request.extend(list(map(lambda x: json.dumps(x), it)))
    try:
        Type, Data = comm.interface_client.send_request('latex', 'get_pdf', Data=doc_request, timeout=2)
    except comm.InterfaceClient.TimeOutExcept:
        return HttpResponse('TeX модуль временно недоступен')
    filename = 'td' + str(random.randint(10000, 99999))
    try:
        os.mkdir('temp', mode=0o777, dir_fd=None)
    except FileExistsError:
        pass
    Data.generate_pdf(filepath='./temp/' + filename)
    filename = filename + '.pdf'
    with open('./temp/' + filename, 'rb') as fin:
        Data = fin.read()
    response = HttpResponse(Data, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    os.remove('./temp/' + filename)
    return response
