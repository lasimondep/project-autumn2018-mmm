import json

def get_json_file(file_name):
    a = ''
    with open('C:\\Users\\akors\\Desktop\\modul\\' + file_name) as task:
        for line in task:
            a += line
    a = json.loads(a)
    print(a)
    b = a["task"]
    task = ''
    flag = 2
    for i in range(len(b)):
        if flag < 2:
            flag += 1
        else:
            if b[i] != "$":
                task += b[i]
            else:
                task += a["$" + b[i+1] + "$"]
                flag = 0
    task = list(task)
    for i in range(len(task)):
        if task[i] == ' ':
            task[i] = '\,'
    return ''.join(task)





