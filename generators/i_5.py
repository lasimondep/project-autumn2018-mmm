import json
import sys
import random
import math


def get_answer(n, values = []):
    A = []
    for i in range(2**n):
        answer = bin(i)[2:]
        for m in range(n - len(answer) + 1):
            flag = 1
            answer = bin(i)[2:].zfill(n-m)
            #print("Result: ", answer)
            for j in range(len(values)):
                y = ""
                if len(answer) >= len(values[j]):
                    for k in range(len(values[j])):
                        y += answer[k]
                    if values[j] == y:
                        flag = 0
                        break
                else:
                    for k in range(len(answer)):
                        y += values[j][k]
                    if answer == y:
                        flag = 0
                        break
            if flag == 1:
                A.append(answer)
    answer = "111111111111111111111"
    #print(A)
    for i in range(len(A)):
        if (len(A[i]) < len(answer)) or (len(A[i]) == len(answer) and A[i] < answer):
            answer = A[i]
        #print("Answer: ", i, answer)
    return answer
        
            
    


    
    #flag1 = 0
    #x_r = 1
    #x_1 = 0
    #while (flag1 == 0):
        #flag2 = 1
        #x = ""
        #for i in range(x_r - x_1):
            #x += "0"
        #for i in range (x_1):
            #x += "1"
        #for i in range(len(values)):
            #y = ""
            #if x == values[i]:
                #flag2 = 0
                #break
            #if len(x) >= len(values[i]):
                #for k in range(len(values[i])):
                    #y += x[k]
                #if values[i] == y:
                    #flag2 = 0
                    #break
            #else:
                #for k in range(len(x)):
                    #y += values[i][k]
                #if x == y:
                    #flag2 = 0
                    #break
        #if flag2 == 1:
            #flag1 = 1
        #else:
            #x_1 += 1
            #if x_1 > x_r:
                #x_r += 1
                #x_1 = 0
    #return x
                
        

def initial_values(m):
    d = {}
    i = 0
    for it in m[1:]:
        key = int(it.split('=')[0])
        value = it.split('=')[1]
        d.update({key:value})
    """
    while i < len(m):
        key = ""
        value = ""
        while (i < len(m)) and (m[i] != "="):
            key += m[i]
            i += 1
        i += 1
        while (i < len(m)) and (m[i] != " "):
            value += m[i]
            i += 1
        i += 1
        d.update({int(key):value})
    """
    alph = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧЪЫЬЭЮЯ"
    values = []
    letters = []
    inserts = [""]*7
    combinations_max = 1
    try:
        for i in range(int(d[1])):
            combinations_max *= 2
        if int(d[2]) > combinations_max-1:
            sys.stderr.write("Error: Недопустимое соотношение букв и разрядов")
            return 0
    except KeyError:
        print('')
    try:                                       #макс кол-во рязрядов
        inserts[0] = int(d[1])
    except KeyError:
        inserts[0] = random.randint(3, 6)
        for i in range(inserts[0]):
            combinations_max *= 2
    try:                                       #кол-во букв
        inserts[1] = int(d[2])
    except KeyError:
        inserts[1] = random.randint(4, 7)
    combinations_number = combinations_max
    min_digit = math.ceil(math.log2(2**(inserts[0])/(2**(inserts[0])-inserts[1])))
    n = -min_digit      
    for i in range(inserts[1]):
        #print("comb_number: ", combinations_number)
        while (math.log2(combinations_number/combinations_max) <= n):
            n -= 1
            min_digit += 1
        flag1 = 0
        while flag1 == 0:
            x = ""
            flag2 = 1
            if min_digit  == inserts[0]:
                for j in range(min_digit):
                    x += str(random.randint(0,1))
            else:
                for j in range(random.randint(min_digit, inserts[0])):
                    x += str(random.randint(0,1))
            #print("Сгенерировано: ", x)
            for j in range(len(values)):
                y = ""
                if len(x) >= len(values[j]):
                    for k in range(len(values[j])):
                        y += x[k]
                    if values[j] == y:
                        flag2 = 0
                        break
                else:
                    for k in range(len(x)):
                        y += values[j][k]
                    if x == y:
                        flag2 = 0
                        break
            if combinations_number <= (inserts[1]-i-1)+2**(inserts[0]-len(x)):
                flag2 = 0
            if flag2 == 1:
                flag1 = 1
                values.append(x)
                combinations_number -= 2**(inserts[0] - len(x))
                #print("Пройдено: ", x)
    for i in range(len(values)):
        letters.append(alph[i])
    for i in range(len(letters)):
        inserts[2] += letters[i] + ", "
        inserts[3] += letters[i] + " - " + values[i] + ","
    inserts[5] = get_answer(inserts[0], values)
    inserts[4] = inserts[2]
    inserts[6] = letters[len(letters)-1]
    for i in range(len(letters)-1):
        inserts[4] += letters[i] + ", "
    return inserts

va = sys.argv
inserts = initial_values(va)

#test = ""
#test += 'Для кодирования некоторой последовательности, состоящей из букв '
#test += inserts[2]
#test += 'решили использовать неравномерный двоичный код, позволяющий однозначно декодировать двоичную последовательность,появляющуюся на приёмной стороне канала связи. Для букв ' 
#test += inserts[4]
#test += 'использовали такие кодовые слова:'
#test += inserts[3]
#test += 'Укажите, каким кодовым словом может быть закодирована буква '
#test += inserts[6]
#test += '. Код должен удовлетворять свойству однозначного декодирования.\
  #Если можно использовать более одного кодового слова, укажите кратчайшее из них, имеющее минимальное значение.'

#print(test)
#print("Ответ: ", inserts[5])

dic = {'text':{'text1':['Для кодирования некоторой последовательности, состоящей из букв ', 'insert1', \
               'решили использовать неравномерный двоичный код, позволяющий однозначно декодировать двоичную последовательность,появляющуюся на приёмной стороне канала связи. Для букв ', \
               'insert2', 'использовали такие кодовые слова:', 'insert3', \
               'Укажите, каким кодовым словом может быть закодирована буква ', 'insert4', '. Код должен удовлетворять свойству однозначного декодирования.\
 Если можно использовать более одного кодового слова, укажите кратчайшее из них, имеющее минимальное значение.']},
       'inserts':{'insert1':inserts[2], 'insert2':inserts[4], 'insert3':inserts[3], 'insert4':inserts[6], 'insert5':inserts[5]},
       'answers':{'text1':['Ответ', 'insert5']}
       }
    
        
print(json.dumps(dic))
