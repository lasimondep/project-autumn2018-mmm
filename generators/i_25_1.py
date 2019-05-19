import random
import sys
import json


def initial_values(m):
    a = ["не делится ", "кратно ", "положительно ", "отрицательно ", "больше ", "меньше "]
    b = ["не делится ", "кратна ", "положительна ", "отрицательна ", "больше ", "меньше "]
    c = [""]*8
    _d = {}
    for i in range (len(m) - 1):
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
        _d.update({int(key):value})
        
        
    try:
        if _d[1] == "не делится" or _d[1] == "кратно" or _d[1] == "положительно" or _d[1] == "отрицательно" or _d[1] == "больше" or _d[1] == "меньше":
            c[0] = _d[1] + " "
        else:
            sys.stderr.write("error:Неверный формат 1 параметра")
    except KeyError:
        c[0] = a[random.randint(0, 5)]
    try:
        if _d[2] == "не делится" or _d[2] == "кратна" or _d[2] == "положительна" or _d[2] == "отрицательна" or _d[2] == "больше" or _d[2] == "меньше":
            c[0] = _d[2] + " "
        else:
            sys.stderr.write("error:Неверный формат 2 параметра\n")
    except KeyError:
        c[1] = b[random.randint(0, 5)]
    try:
        try:
            c[2] = int(_d[3])
        except KeyError:
            if (c[0] == "не делится ") or (c[0] == "кратно "):
                c[2] = str(random.randint(2, 100))
                if c[0] == "не делится":
                    c[4] = "mod " + c[2] + " <> 0"
                    c[6] = "%" + c[2] + "!= 0"
                else:
                    c[4] = "mod " + c[2] + " == 0"
                    c[6] = "%" + c[2] + "== 0"
            elif (c[0] == "больше ") or (c[0] == "меньше "):
                c[2] = str(random.randint(-100, 100))
                if c[0] == "больше ":
                    c[4] = "> " + c[2]
                    c[6] = "> " + c[2]
                else:
                    c[4] = "< " + c[2]
                    c[6] = "< " + c[2]
            else:
                c[2] = ""
                if c[0] == "положительно ":
                    c[4] = "> 0"
                    c[6] = "> 0"
                else:
                    c[4] = "< 0"
                    c[6] = "< 0"
    except ValueError:
        sys.stderr.write("error:Неверный формат 3 параметра")
    try:
        try:
            c[3] = int(_d[4])
        except KeyError:
            if (c[1] == "не делится ") or (c[1] == "кратно "):
                c[3] = str(random.randint(2, 100))
                if c[1] == "не делится":
                    c[5] = "mod " + c[3] + " <> 0"
                    c[7] = "%" + c[3] + "!= 0"
                else:
                    c[5] = "mod " + c[3] + " == 0"
                    c[7] = "%" + c[3] + "== 0"
            elif (c[1] == "больше ") or (c[1] == "меньше "):
                c[3] = str(random.randint(-100, 100))
                if c[1] == "больше ":
                    c[5] = "> " + c[3]
                    c[7] = "> " + c[3]
                else:
                    c[5] = "< " + c[3]
                    c[7] = "< " + c[3]
            else:
                c[3] = ""
                if c[1] == "положительно ":
                    c[5] = "> 0"
                    c[7] = "> 0"     
                else:
                    c[5] = "< 0"
                    c[7] = "< 0"
    except ValueError:
        sys.stderr.write("error:Неверный формат 4 параметра")
    if (c[0] == "положительно " or c[0] == "отрицательно ") or (c[1] == "положительна " or c[1] == "отрицательна "):
        if c[2] != "" and c[3] != "":
            sys.exit("error:Неверный формат") 
    return c

            
va = sys.argv
c = initial_values(va)


dict1 = {'text':{'text1':['Дан целочисленный массив из 40 элементов. \
                Элементы массива могут принимать целые значения от –100 до 100 включительно.\n \
                Опишите на естественном языке или на одном из языков программирования алгоритм, позволяющий найти и вывести количество пар элементов массива, произведение которых ',
                'insert1', ', а сумма', 'insert2',
                '.\nПод парой подразумевается два подряд идущих элемента массива.'],
                'table1':{'row1':{'col1':['Паскаль'], 'col2':['Python'], 'col3':['Си']}, \
                          'row2':{'col1':['const n = 40;\n var\n  a: array [0..n-1]\n     of integer;\n  i, j, k: integer;\nbegin\n  for i:=0 to n-1 do\n     readln(a[i]);\n  ...\nend.'], \
                                  'col2':['# допускается также\n# использовать две\n# целочисленные\n# переменные j, k\na = []\nn = 40\nfor i in range(n):\n  a.append(int(input()))\n...'], \
                                  'col3':['#include <stdio.h>\n#define n 40\nint main() {\n  int a[n];\n  int i, j, k;\n  for (i = 0; i < n; i++)\n    scanf(\"%d\", &a[i]);\n  ...\n  return 0;\n}']
                                 }
                         }
                },
         'inserts':{'insert1':c[0], 'insert2':c[1], 'insert3':c[2], 'insert4':c[3], 'insert5':c[4], 'insert6':c[5], 'insert7':c[6], 'insert8':c[7]},
         'answers':{'table1':{'row1':{'col1':['k := 0;\n for i:=0 to n-2 do\n  if ((a[i]*a[i+1]) ', 'insert5', ') and (a[i]+a[i+1] ', 'insert6', ') then\n    k := k + 1;\nwriteln(k);'], \
                                      'col2':["k = 0\nfor i in range(n-1)\n  if ((a[i]*a[i+1]) ", 'insert7', ") and (a[i]+a[i+1] ", 'insert8', ")):\n    k += 1\nprint(k)"], \
                                      'col3':["k = 0;\nfor(i=0;i<n-1;i++)\n  if ((a[i]*a[i+1]) ", 'insert7', " && (a[i]+a[i+1]", 'insert8', "))\n    k ++;\nprintf(\"%d\", k);"]
                                     }
                             }
                    }
         }

print(json.dumps(dict1))

    
          