import random
import sys
import json

def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
va = sys.argv

if len(va)==1:
    R = random.randint(71, 121)
else:
    if int(va[1].split("=")[0]) == 1:
        l = (va[1].split("="))[1]
        if is_int(l) and 50<int(l)<150:
            R=int(l)
        else:
            sys.exit("error")
    else:
        sys.exit("error")
R1=R
R+=1
r=(bin(R))[2:]
s=0
for i in range(len(r)-2):
    s=s+int(r[i])

flag=" "
while flag!="Ok":
    if r[-2:]=="00":
        if is_int(R/4) and s%2==0:
            answer=R/4
            flag = "Ok"
    elif r[-2:]=="10" and s%2==1:
        if is_int((R-2)/4):
            answer=(R-2)/4
            flag = "Ok"
    R+=1
    r=(bin(R))[2:]
str1="На вход алгоритма подаётся натуральное число N. Алгоритм строит по нему новое число R следующим образом."
str2="\n\t1.	Строится двоичная запись числа N."
str3="\n\t2.	К этой записи дописываются справа ещё два разряда по следующему правилу:"
str4="\n\t\tа)	складываются все цифры двоичной записи, и остаток от деления суммы на 2 дописывается в конец числа (справа). Например, запись 10000 преобразуется в запись 100001;"
str5="\n\t\tб)	над этой записью производятся те же действия — справа дописывается остаток от деления суммы цифр на 2."
str6="\nПолученная таким образом запись (в ней на два разряда больше, чем в записи исходного числа N) является двоичной записью искомого числа R."
str7="\nУкажите такое наименьшее число N, для которого результат работы алгоритма больше "+str(R1)+". В ответе это число запишите в десятичной системе счисления."
st0=str1+str2+str3+str4+str5+str6+str7
json_dict = {'text' : {}, 'answers': {}, 'inserts' : {}}
str8="\nУкажите такое наименьшее число N, для которого результат работы алгоритма больше "
str9=". В ответе это число запишите в десятичной системе счисления."
text1 = [(str1+str2+str3+str4+str5+str6+str8)]
text1 += ["insert1"]
text1 += [str9]
json_dict['text'].update({"text1":text1})
json_dict['answers'].update({"text1":["Ответ","insert2"]})
json_dict['inserts'].update({"insert1":str(R1)})
json_dict['inserts'].update({"insert2":str(answer)})
print(json_dict['inserts'])

f2=json.dumps(json_dict)
print(f2)
