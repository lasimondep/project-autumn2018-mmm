# Задача первого типа: операющиеся на несколько предедыдущих значений
import random
import sys
import json

def is_int (str):
    try:
        int(str)
        return True
    except ValueError:
        return False
def generate(i,a,b,f):
    if i == 1:#генерация f[0]
        f[0]=random.randint(0, 2)
        return(f[0])
    elif i == 2:#генерация f[1]
        f[1] = random.randint(1, 4)
        return(f[1])
    elif i==3:
        return ( random.randint(1,5))# генерация a
    elif (i == 4):
        return(random.randint(0, 1))
    elif i==5:
        return (random.randint(1, 4))# генерация b
    elif i==6:
        if (a >= 3 or b >= 3):
            return( random.randint(5, 6))# генерация n
        else:
            return( random.randint(5, 12))
def gen2(f,a,i,b,n):
    if (i == 1):
        znak = "+"
        for i in range(2, n):
            f.append (a * f[i - 1] + b * f[i - 2])
    else:
        znak = "-"
        for i in range(2, n):
            f.append(a * f[i - 1] - b * f[i - 2])
    json_dict = {'text': {'text1': []}, 'answers': {'text1':[]}, 'inserts': {}}
    json_dict['text']['text1'] += ["Алгоритм вычисления значения функции F(n), где n - натуральное число:  \nF(1)="]
    json_dict['text']['text1'] += ["insert1"]  # f[0]
    json_dict['text']['text1'] += ["\nF(2)="]
    json_dict['text']['text1'] += ["insert2"]  # f[1]
    json_dict['text']['text1'] += ["\nF(n)="]
    json_dict['text']['text1'] += ["insert3"]  # a
    json_dict['text']['text1'] += ["*F(n-1)"]
    json_dict['text']['text1'] += ["insert4"]  # znak
    json_dict['text']['text1'] += ["insert5"]  # b
    json_dict['text']['text1'] += ["*F(n-2),  при n>2.\n Чему равно значение функции F("]
    json_dict['text']['text1'] += ["insert6"]  # n
    json_dict['text']['text1'] += [")?\nВ ответе запишите только натуральное число."]
    json_dict['inserts'].update({'insert1':str(f[0])})
    json_dict['inserts'].update({'insert2': str(f[1])})
    json_dict['inserts'].update({'insert3': str(a)})
    json_dict['inserts'].update({'insert4': znak})
    json_dict['inserts'].update({'insert5':str(b)})
    json_dict['inserts'].update({'insert6': str(n)})
    json_dict['inserts'].update({'insert7': str(f[n-1])})
    json_dict['answers'].update({'text1':['Ответ: ', 'insert7']})
    # st = "Алгоритм вычисления значения функции F(n), где n - натуральное число:  \nF(1)=" + str(f[0]) + "\nF(2)="\
    #          + str(f[1]) + "\n" + "F(n)=" + str(a) + "*F(n-1)" + znak + str(b) + "*F(n-2)" + "  при n>2" + "\n" \
    #          + "Чему равно значение функции F(" + str(n) + ")?" + "\n" + "В ответе запишите только натуральное число."
    # print(st)
    # print(f[n - 1])
    # print(json_dict['text'])
    # print(json_dict['inserts'])
    # print(json_dict['answers'])
    #print(json_dict)
    print(json.dumps(json_dict))
    return
#main
f = [0 for i in range(2)]
_d = dict()
m=[0,0,0,0,0,0]
for sarg in sys.argv[1:]:
    key, value = sarg.split("=")
    key=int(key)
    _d.update({key:value})
for i in range(1,7):
    if  _d.get(i)==None:
        m[i - 1] = generate(i, m[2], m[4], f)
    else:
        if (i == 4):
            if _d[4] == "+":
                m[3] = 1
            elif (_d[4] == "-"):
                m[3] = 0
            else:
                sys.stderr.write("error:Неверный формат ввода!")
        else:
            if (is_int(_d[i])):
                m[i - 1] = int(_d[i])
                if (i == 1) or (i == 2):
                    f[i-1] = m[i - 1]
            else:
                sys.stderr.write("error: Неверный формат ввода!")
#вызов функции
gen2(f,m[2],m[3],m[4],m[5])




