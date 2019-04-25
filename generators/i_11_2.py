# Задача первого типа: операющиеся на несколько предедыдущих значений (3)

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
    if i==1:
        f[0] = random.randint(0, 2)
        return (f[0])# генерация F(1)
    elif i==2:
        f[1]=random.randint(1, 3)
        return (f[1])#генерация F(2)
    elif i==3:
        f[2]=random.randint(1, 4)
        return (f[2])#генерация F(3)
    elif i == 4:
        return (random.randint(1, 5))  # генерация a
    elif (i == 5):
        return (random.randint(0, 1))
    elif i == 6:
        return (random.randint(1, 4))  # генерация b
    elif i == 7:
        if (a >= 3 or b >= 3):
            return (random.randint(5, 6))  # генерация n
        else:
            return (random.randint(5, 12))




def gen3(f, a, i, b, n):
    if (i == 1):
        znak = "+"
        for i in range(3, n):
            f.append(a * f[i - 2] + b * f[i - 3])
            # print(f[i])
    else:
        znak = "-"
        for i in range(2, n):
            f.append( a * f[i - 2] - b * f[i - 3])
            # print(f[i])
    json_dict = {'text': {'text1': []}, 'answers': {'text1': []}, 'inserts': {}}
    json_dict['text']['text1'] += ["Алгоритм вычисления значения функции F(n), где n - натуральное число:  \nF(1)="]
    json_dict['text']['text1'] += ["insert1"]  # f[0]
    json_dict['text']['text1'] += ["\nF(2)="]
    json_dict['text']['text1'] += ["insert2"]  # f[1]
    json_dict['text']['text1'] += ["\nF(3)="]
    json_dict['text']['text1'] += ["insert3"]
    json_dict['text']['text1'] += ["\nF(n)="]
    json_dict['text']['text1'] += ["insert4"]  # a
    json_dict['text']['text1'] += ["*F(n-1)"]
    json_dict['text']['text1'] += ["insert5"]  # znak
    json_dict['text']['text1'] += ["insert6"]  # b
    json_dict['text']['text1'] += ["*F(n-2),  при n>3.\n Чему равно значение функции F("]
    json_dict['text']['text1'] += ["insert7"]  # n
    json_dict['text']['text1'] += [")?\nВ ответе запишите только натуральное число."]
    json_dict['inserts'].update({'insert1': str(f[0])})
    json_dict['inserts'].update({'insert2': str(f[1])})
    json_dict['inserts'].update({'insert3': str(f[2])})
    json_dict['inserts'].update({'insert4': str(a)})
    json_dict['inserts'].update({'insert5': znak})
    json_dict['inserts'].update({'insert6': str(b)})
    json_dict['inserts'].update({'insert7': str(n)})
    json_dict['inserts'].update({'insert8': str(f[n - 1])})
    json_dict['answers'].update({'text1': ['Ответ: ', 'insert8']})
    # st = "Алгоритм вычисления значения функции F(n), где n - натуральное число:  \nF(1)=" + str(f[0]) + "\nF(2)=" \
    #      + str(f[1])+"\nF(3)=" + str(f[2]) + "\n" + "F(n)=" + str(a) + "*F(n-2)" + znak + str(b) + "*F(n-3)" + "  при n>3" + "\n" \
    #      + "Чему равно значение функции F(" + str(n) + ")?" + "\n" + "В ответе запишите только натуральное число."
    # print(st)
    print(json.dumps(json_dict))
    return

#генерирование входных данных
f = [0 for i in range(3)]
_d = dict()
m=[0,0,0,0,0,0,0]
for sarg in sys.argv[1:]:
    key, value = sarg.split("=")
    key=int(key)
    _d.update({key:value})
for i in range(1,8):
    if  _d.get(i)==None:
        m[i - 1] = generate(i, m[3], m[5], f)
    else:
        if (i == 5):
            if _d[5] == "+":
                m[4] = 1
            elif (_d[5] == "-"):
                m[4] = 0
            else:
                sys.stderr.write("error:Неверный формат ввода!")
        else:
            if (is_int(_d[i])):
                m[i - 1] = int(_d[i])
                if (i == 1) or (i == 2)or(i==3):
                    f[i-1] = m[i - 1]
            else:
                sys.stderr.write("error: Неверный формат ввода!")

#вызов функции


gen3(f,m[3],m[4],m[5],m[6])