import json
import re

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat
from pylatex.utils import italic
import os

from common import AMQP_client


class MyClient(AMQP_client):
    def parse(self, Id, Type, Data):
        if Type == "post_task":
            tex_string = func(Data)
            self.send('interface', Id, 'post_tex', tex_string)

client = MyClient('localhost', 'latex')
client.start_consume()
print('I`m start')
try:
    while True:
        pass
except KeyboardInterrupt:
    client.stop_consume()
    print("Close connection & stop thread")

def fill_document(doc, json_in, flag):
    pattern = r'insert\d'
    pat = ''
    for i in json_in['text']:
        case = re.findall(pattern, i)
        #print(type(case))
        for i in case:
            pat = i
        if i != pat:
            doc.append(i + ' ')
        else:
            doc.append(json_in['inserts'][i] + ' ')

    if flag:
        for i in json_in['answers']:
            case = re.findall(pattern, i)
            # print(type(case))
            for i in case:
                pat = i
            if i != pat:
                doc.append(i + ' ')
            else:
                doc.append(json_in['inserts'][i] + ' ')
    return

def modify_str(str):
    str_list = str.split()
    print(str_list)
    interface_str = ''
    flag = False
    for i in str_list:
        if i =='\\begin{document}%':
            flag = True
            continue
        if flag:
            if i == '\\end{document}':
                break
            interface_str += i + ' '
    return interface_str

def func(data):
    json_in = json.loads(data)
    flag = True

    geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
    doc = Document(geometry_options=geometry_options)
    fill_document(doc, json_in, flag)

    tex = doc.dumps()
    tex = r'\usepackage[english, russian]{babel}' + '\n' + tex
    str = modify_str(tex)
    with open('output.tex', 'w') as tex_out:
        for line in tex:
            tex_out.write(line)
    # doc.generate_pdf('full', clean_tex=False)
    return str

# if __name__ == '__main__':
#     json_in = {'text': ['Сложите число', 'insert1', 'с числом', 'insert2', '. Ответ запишите в виде двоичного кода.\n'],
#                'answers': ['Ответ:', 'insert3'],
#                'inserts': {'insert1': '322', 'insert2': '228', 'insert3': '550'}
#     }
#     tex = ''
#     str = ''
#     flag = True
#
#     geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
#     doc = Document(geometry_options=geometry_options)
#     fill_document(doc, json_in, flag)
#
#     tex = doc.dumps()
#     tex = r'\usepackage[english, russian]{babel}' +'\n' + tex
#     str = modify_str(tex)
#     #print(tex)
#     print(str)
#     with open('output.tex', 'w') as tex_out:
#         for line in tex:
#             tex_out.write(line)
#     #doc.generate_pdf('full', clean_tex=False)
