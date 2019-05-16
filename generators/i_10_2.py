import random
import json
import sys
va = sys.argv
def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
if len(va)==1:
    n1 = 5
else:
    l1 = (va[1].split("="))[1]
    if is_int(l1) and 4<=int(l1)<=6:
        n1=int(l1)
    else:
        sys.exit("error")
ls=list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧЪЫЬЭЮЯ") 
base=n1
p=[] 
N=n=random.randint(100,250) 
for i in range(base): 
    l=random.choice(ls) 
    p+=l 
    ls.remove(l) 

newn = '' 
while n > 0: 
    newn = str(n % base) + newn 
    n //= base 

answer1=''
answer='' 
for i in newn : answer1+=p[int(i)]
if len(answer1)<base:
    for i in range(base-len(answer1)): answer+=(p[0])
answer+=answer1

st='' 
for i in range(base): 
    st+=str(i+1)+". " 
    for j in range(base-1): 
        st+=str(p[0]) 
    st+=str(p[i])+"\n" 
st+=str(base+1)+". " 
for i in range(base-2):st+=str(p[0]) 
st+=str(p[1])+str(p[0])+"\n......." 

stt='' 
stt+="\tВсе "+str(base)
st1="-буквенные слова, составленные из букв "+str(p)+ " записаны в алфавитном порядке и пронумерованы. Вот начало списка:\n" 
stt+=st1
st2="\n"+"\tНа каком месте от начала списка стоит слово " + answer + " ?"
stt+=st+st2
#print(stt) 
#print("Ответ: "+str(N))
#f=json.dumps(stt)

json_dict = {'text' : {}, 'answers': {}, 'inserts' : {}}
text1=["\tВсе ","insert1",(st1+st+st2)]
json_dict['text'].update({"text1":text1})
json_dict['answers'].update({"text1":["Ответ","insert2"]})
json_dict['inserts'].update({"insert1":str(base)})
json_dict['inserts'].update({"insert2":str(N)})

print(json_dict)


















