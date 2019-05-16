import random
import json
import sys
A=[]
st=''
va = sys.argv
def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
if len(va)==1:
    n = 10
else:
    l = (va[1].split("="))[1]
    if is_int(l) and 8<int(l)<15:
        n=int(l)+1
    else:
        sys.exit("error")

for i in range(n):
    A.append(random.randint(0,100))
    st+=str(A[i])+', '

#k1=random.randint(2,3)
k1=3
#k2=random.randint(1,2)
k2=1
s = 0
for i in range(k1,n):
    s = s + A[i]**k2 - A[i-k1+1]**k2

st0=''
st0+="В программе используется фрагмент одномерного целочисленного массив A с индексами от 0 до "
st01=". Значения элементов равны "
st01+=st+"т. е. A[0] = "+str(A[0])+", A[1] = "+str(A[1])+" и т. д."
st01+="\nОпределите значение переменной s после выполнения следующего фрагмента этой программы (записанного ниже на трёх языках программирования).\n"


#st1='Python\n'
st1="s = 0\nn = "+str(n)+"\nfor i in range("+str(k1)+",n):\n\ts = s + "
if k2==2:
    st1+="A[i]*A[i]-A[i-"+str(k1-1)+"]*A[i-"+str(k1-1)+"]"
else:  st1+="A[i]-A[i-"+str(k1-1)+"]"


#st2="Си\n"
st2="s = 0;\nn = "+str(n)+";\nfor (i="+str(k1)+";i<n; i++){\n\ts = s + "
if k2==2:
    st2+="A[i]*A[i]-A[i-"+str(k1-1)+"]*A[i-"+str(k1-1)+"];"
else:  st2+="A[i]-A[i-"+str(k1-1)+"];"
st2+="\n}\n"

#st3="Паскаль\n"
st3="s := 0;\nn := "+str(n)+";\nfor i:="+str(k1)+" to n-1 do begin\n\ts := s + "
if k2==2:
    st3+="A[i]*A[i]-A[i-"+str(k1-1)+"]*A[i-"+str(k1-1)+"];"
else:  st3+="A[i]-A[i-"+str(k1-1)+"];"
st3+="\nend;\n"

json_dict = {'text' : {}, 'answers': {}, 'inserts' : {}}
text1=[st0,"insert1",st01]
json_dict['text'].update({"text1":text1})
table1={'row1':{'col1':['Python'], 'col2':['Си'], 'col3':['Паскаль']}}
table1.update({'row2':{'col1':[st1], 'col2':[st2], 'col3':[st3]}})
json_dict['text'].update({"table1":table1})
json_dict['answers'].update({"text1":["Ответ","insert2"]})
json_dict['inserts'].update({"insert1":str(n-1)})
json_dict['inserts'].update({"insert2":str(s)})
#print(json_dict)
f2=json.dumps(json_dict)
print(f2)

#S=st0+st1+"\n"+st2+"\n"+st3
#print(S)
#print("\n"+str(s))
