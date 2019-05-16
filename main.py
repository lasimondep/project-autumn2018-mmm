import json
import re
from pylatex import *
from common import AMQP_client


def modify_str(str1, Type):
    pattern1 = r'insert\d{,100}'
    str1 = str1.replace('\{\{', '{')
    str1 = str1.replace('\}\}', '}')
    str1 = str1.replace('{-}', '-')
    str1 = str1.replace('\&\&\&', '&')
    str1 = str1.replace(r'\textbackslash{}', '\\')
    interface_str = ''
    flag = False
    flag1 = False

    if Type == "get_task_text" or Type == "get_task":
        str1 = str1.replace('%', '')
        str1 = str1.replace(r'\normalsize', '')
        str1_list = str1.splitlines()
        temp_str = ''
        interface_str = []

        for i in str1_list:
            if i == '\\begin{document}':
                flag = True
                continue
            if flag:
                if i == r'\begin{array}{|l|l|l|}':
                    flag1 = True
                if i ==r'\end{array}':
                    flag1 = False
                if flag1:
                    i = i.replace(r'\newline', r'\\')
                    i = i.replace('<', '{<}')
                else:
                    i = i.replace(r'\newline', r'<br>')
                match1 = re.findall(pattern1, i)
                if match1:
                    str1 = re.findall(pattern1, i)[0]
                    interface_str += [temp_str] + [i.replace(str1, '')]
                    temp_str = ''
                elif i == '\\end{document}':
                    interface_str += [temp_str]
                    break
                else:
                    temp_str += i + ' '

    if Type == "get_pdf":
        str1_list = str1.splitlines()
        for i in str1_list:
            if i == r'\begin{array}{|l|l|l|}%':
                flag = True
            if flag:
                i = i.replace(r'\newline', r'\\')
                if i == '\end{array}%':
                    flag = False
            interface_str += i + ' \n'

    if Type == "post_task":
        str1 = str1.replace('%', '')
        str1 = str1.replace(r'\newline', r'\\')
        str1 = str1.replace(r'\normalsize', '')
        str1_list = str1.splitlines()
        for i in str1_list:
            if i == '\\begin{document}':
                flag = True
                continue
            if flag:
                i = i.replace(r'\newline', '\n')
                if i == '\\end{document}':
                    break
                interface_str += i + ' '
    return interface_str


def func(data, Type):
    json_in = data
    flag = False
    tex = ''
    geometry_options = {"tmargin": "2cm", "lmargin": "2cm"}

    if Type == "post_task":
        doc = []
        tex = []

        for i in range(len(json_in)):
            doc.append(Document(geometry_options=geometry_options))
            doc[i].preamble.append(Command('usepackage[english, russian]', 'babel'))
        fill_document(doc, json_in, flag)

        for i in range(len(json_in)):
            tex.append(doc[i].dumps())
            tex[i] = modify_str(tex[i], Type)

    elif Type == 'get_pdf':
        geometry_options = {"tmargin": "2cm", "lmargin": "2cm"}
        doc = Document(geometry_options=geometry_options)
        doc.preamble.append(Command('usepackage[english, russian]', 'babel'))
        pdf_generate(doc, json_in, flag)
        tex = doc
        # tex = modify_str(tex, Type)
        # tex = doc.dumps()

    elif Type == 'get_task_text' or Type == "get_task":
        doc = []
        tex = []
        for i in range(len(json_in)):
            doc.append(Document(geometry_options=geometry_options))
            doc[i].preamble.append(Command('usepackage[english, russian]', 'babel'))
        without_inserts(doc, json_in)

        for i in range(len(json_in)):
            tex.append(doc[i].dumps())
            tex[i] = modify_str(tex[i], Type)
    return tex


def without_inserts(doc, json_in):
    pattern1 = r'insert\d{,100}'
    pattern2 = r'text\d{,100}'
    pattern3 = r'table\d{,100}'

    for i in range(len(doc)):
        for key in json_in[i]['text']:
            text1 = re.fullmatch(pattern2, key)
            table1 = re.fullmatch(pattern3, key)

            if text1:
                for text in json_in[i]['text'][key]:
                    match1 = re.findall(pattern1, text)
                    if match1:
                        doc[i].append(json_in[i]['inserts'][text]+ text)
                    else:
                        doc[i].append(text + ' ')

            if table1:
                rows = []
                for row in json_in[i]['text'][key]:
                    cols = []
                    for col in json_in[i]['text'][key][row]:
                        cols.append(json_in[i]['text'][key][row][col][0])
                    rows.append(cols)
                for j in range(3):
                    rows[1][j] = rows[1][j].replace(' ', '\;')
                doc[i].append('\n\n')
                doc[i].append(Command('begin{array}', '|l|l|l|'))
                doc[i].append(Command('hline'))
                doc[i].append(r'Паскаль &&& Python &&& C++ \\')
                doc[i].append(Command('hline'))
                doc[i].append('{{' + rows[1][0] + '}}' + ' &&& ' + '{{' + rows[1][1] + '}}' + ' &&& ' + '{{' + rows[1][2] + r'}} \\')
                doc[i].append(Command('hline'))
                doc[i].append(Command('end', 'array'))
    return


def pdf_generate(doc, json_in, flag):
    pattern1 = r'insert\d{,100}'
    pattern2 = r'text\d{,100}'
    pattern3 = r'table\d{,100}'

    for i in range(len(json_in)):
        doc.append('~\n\n\tЗадача' + str(i+1) + ':\n')
        for key in json_in[i]['text']:
            match = re.fullmatch(pattern2, key)
            table1 = re.fullmatch(pattern3, key)

            if match:
                for text in json_in[i]['text'][key]:
                    match1 = re.findall(pattern1, text)
                    if match1:
                        doc.append(json_in[i]['inserts'][text] + ' ')
                    else:
                        doc.append(text + ' ')

            if table1:
                rows = []
                for row in json_in[i]['text'][key]:
                    cols = []
                    for col in json_in[i]['text'][key][row]:
                        cols.append(json_in[i]['text'][key][row][col][0])
                    rows.append(cols)
                doc.append(Command('begin{enumerate}'))
                for i in range(len(rows[0])):
                    doc.append(Command('item'))
                    doc.append(rows[0][i])
                    doc.append(Command('newline'))
                    doc.append(rows[1][i])
                doc.append(Command('end', 'enumerate'))
                # for j in range(3):
                #     rows[1][j] = rows[1][j].replace(' ', '\;')
                # # print(rows)
                # doc.append('\n\n')
                # doc.append(Command('begin{array}', '|l|l|l|'))
                # doc.append(Command('hline'))
                # doc.append(r'Паскаль &&& Python &&& C++ \\')
                # doc.append(Command('hline'))
                # doc.append('{{' + rows[1][0] + '}}' + ' &&& ' + '{{' + rows[1][1] + '}}' + ' &&& ' + '{{' + rows[1][
                #     2] + r'}} \\')
                # doc.append(Command('hline'))
                # doc.append(Command('end', 'array'))

        if flag:
            for text in json_in[i]['answers']:
                match1 = re.findall(pattern1, text)
                if match1:
                    doc.append(json_in[i]['inserts'][text] + ' ')
                else:
                    doc.append(text + ' ')
    return


def fill_document(doc, json_in, flag):
    pattern1 = r'insert\d{,100}'
    pattern2 = r'text\d{,100}'
    pattern3 = r'table\d{,100}'

    for i in range(len(json_in)):
        for key in json_in[i]['text']:
            text1 = re.fullmatch(pattern2, key)
            if text1:
                for text in json_in[i]['text'][key]:
                    match1 = re.findall(pattern1, text)
                    if match1:
                        doc[i].append(json_in[i]['inserts'][text] + ' ')
                    else:
                        doc[i].append(text + ' ')
            elif table:
                doc.append(Command('begin{array}', '|l|l|l|'))
                rows = []
                doc.append('\n\n')
                for row in json_in[i]['text'][key]:
                    cols = []
                    for col in json_in[i]['text'][key][row]:
                        cols.append(json_in[i]['text'][key][row][col][0])
                    rows.append(cols)
                for i in range(len(rows)+1):
                    doc.append(rows[0][i])
                    doc.append('\n')
                    doc.append(rows[1][i])
                    doc.append('\n\n')
                doc.append(Command('end', 'array'))

        if flag:
            for text in json_in[i]['answers']:
                match1 = re.findall(pattern1, text)
                if match1:
                    doc[i].append(json_in[i]['inserts'][text] + ' ')
                else:
                    doc[i].append(text + ' ')
    return


class TexClient(AMQP_client):
    def parse(self, Id, Type, Data):
        if Type == "post_task":
            json_out = {}
            tex_lst = []
            for i in range(len(Data)):
                tex_lst.append(json.loads(Data[i]))
            dct = tex_lst
            tex_lst = func(tex_lst, Type)
            json_out.update({'non_tex': dct, 'tex': tex_lst})
            json_out = json.dumps(json_out)
            self.send('interface', Id, 'post_tex', json_out)

        if Type == "get_pdf":
            tex_in = []
            for i in range(len(Data)):
                tex_in.append(json.loads(Data[i]))
            json_tex = func(tex_in, Type)
            self.send('interface', Id, 'get_pdf', json_tex)

        if Type == "get_task_text" or Type == "get_task":
            json_text = []
            for index in range(len(Data)):
                json_text.append(json.loads(Data[index]['json']))
            tex_lst = func(json_text, Type)
            for i in range(len(Data)):
                Data[i].update({'json': json.dumps(tex_lst[i])})
                Data[i].update({'raw': json.dumps(json_text[i])})
            self.send('interface', Id, 'tex_task_text', Data)



client = TexClient('localhost', 'latex')
client.start_consume()
print('I`m start')
try:
    while True:
        pass
except KeyboardInterrupt:
    client.stop_consume()
    print("Close connection & stop thread")


# if __name__ == '__main__':
#     json_in = [{'task_id': '1m', 'json': {
#         'text': {'text1': ['Сложите число', 'insert1', 'с числом', 'insert2', '.  Ответ запишите в виде двоичного кода.']},
#         'answers': ['Ответ', 'insert3'],
#         'inserts': {'insert1': '322',
#                     'insert2': '228',
#                     'insert3': '550'}}}, {'task_id': '2i', 'json': {'text':{'text1':['Дан целочисленный массив из 40 элементов. Элементы массива могут принимать целые значения от –100 до 100 включительно.\nОпишите на естественном языке или на одном из языков программирования алгоритм, позволяющий найти и вывести количество пар элементов массива, произведение которых ',
#                 'insert1', ', а сумма', 'insert2',
#                 '.\nПод парой подразумевается два подряд идущих элемента массива.'],
#                 'table1':{'row1':{'col1':['Паскаль'], 'col2':['Python'], 'col3':['Си']},
#                           'row2':{'col1':['const n = 40;\nvar\na: array [0..n-1]\nof integer;\ni, j, k: integer;\nbegin\nfor i:=0 to n-1 do\nreadln(a[i]);\n...\nend.'],
#                                   'col2':['# допускается также\n# использовать две\n# целочисленные\n# переменные j, k\na = []\nn = 40\nfor i in range(n):\n  a.append(int(input()))\n...'],
#                                   'col3':['#include <stdio.h>\n#define n 40\nint main() {\nint a[n];\nint i, j, k;\nfor (i = 0; i < n; i++)\nscanf(\"%d\", &a[i]);\n...\nreturn 0;\n}']
#                                  }
#                          }
#                 },
#          'inserts':{'insert1':'12', 'insert2':'23', 'insert3':'24', 'insert4':'34', 'insert5':'12', 'insert6':'4', 'insert7':'2', 'insert8':'22'},
#          'answers':{'table1':{'row1':{'col1':['k := 0;\n for i:=0 to n-2 do\n  if ((a[i]*a[i+1]) ', 'insert5', ') and (a[i]+a[i+1] ', 'insert6', ') then\n    k := k + 1;\nwriteln(k);'],
#                                       'col2':["k = 0\nfor i in range(n-1)\n  if ((a[i]*a[i+1]) ", 'insert7', ") and (a[i]+a[i+1] ", 'insert8', ")):\n    k += 1\nprint(k)"],
#                                       'col3':["k = 0;\nfor(i=0;i<n-1;i++)\n  if ((a[i]*a[i+1]) ", 'insert7', " && (a[i]+a[i+1]", 'insert8', "))\n    k ++;\nprintf(\"%d\", k);"]
#                                      }
#                              }
#                     }
#     }}]
#     # print(json_in)
#     tex = []
#     tex_out = ''
#     flag = True
#     json_text = []
#     for i in range(len(json_in)):
#         json_text.append(json_in[i]['json'])
#     print(json_text)
#
#
#
#     # Type = "get_task_text"
#     #
#     # for index in range(len(json_in)):
#     #     json_text.append(json_in[index]['json'])
#     # tex_lst = func(json_text, Type)
#     # for i in range(len(json_in)):
#     #     json_in[i].update({'json': json.dumps(tex_lst[i])})
#     # print(json_in)
#     #
#     # tex_lst = func(json_text, Type)
#     # json_out = json.dumps(tex_lst)
#     # print(tex_lst)
#     #
#     # with open('output.tex', 'w') as tex_out:
#     #     for i in tex_lst:
#     #         for line in i:
#     #             tex_out.write(line)
#     #             tex_out.write('\n')
#
#     Type = "get_pdf"
#     tex_out = func(json_text, Type)
#     # json_out = json.dumps(tex_out)
#     print(tex_out)
#
#     for i in tex_out:
#         for line in i:
#             print(line, end='')
#
#     with open('output.tex', 'w') as tout:
#         for i in tex_out:
#             tout.write(i)
