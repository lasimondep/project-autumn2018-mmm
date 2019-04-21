import json
import re
import os

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat

from common import AMQP_client


class MyClient(AMQP_client):
    def parse(self, Id, Type, Data):
        if Type == "post_task":
            json_out = {}
            tex_lst = func(Data)
            json_out.update({'non_tex': Data, 'tex': tex_lst})
            json_out = json.dumps(json_out)
            self.send('interface', Id, 'post_tex', json_out)


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
    pattern1 = r'insert\d{,100}'
    pattern2 = r'text\d{,100}'
    pat = ''
    for i in range(len(doc)):
        for key in json_in[i]['text']:
            match = re.fullmatch(pattern2, key)
            if match:
                for text in json_in[i]['text'][key]:
                    match1 = re.findall(pattern1, text)
                    if match1:
                        doc[i].append(json_in[i]['inserts'][text] + ' ')
                    else:
                        doc[i].append(text + ' ')

        if flag:
            for text in json_in[i]['answers']:
                match1 = re.findall(pattern1, text)
                if match1:
                    doc[i].append(json_in[i]['inserts'][text] + ' ')
                else:
                    doc[i].append(text + ' ')
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
    doc = []
    tex = []
    str = ''
    flag = True

    geometry_options = {"tmargin": "2cm", "lmargin": "2cm"}
    for i in range(len(json_in)):
        doc.append(Document(geometry_options=geometry_options))
    fill_document(doc, json_in, flag)
    for i in range(len(json_in)):
        tex.append(doc[i].dumps())
        tex[i] = r'\usepackage[english, russian]{babel}' + '\n' + tex[i]
        tex[i] = modify_str(tex[i])
        #print(str)
    return tex


# if __name__ == '__main__':
#     json_in = [{
#         'text': {'text1': ['Сложите число', 'insert1', 'с числом', 'insert2', '. Ответ запишите в виде двоичного кода.']},
#         'answers': ['Ответ', 'insert3'],
#         'inserts': {'insert1': '322',
#                     'insert2': '228',
#                     'insert3': '550'}},
#         {
#             'text': {'text1': ['Сложите число', 'insert1', 'с числом', 'insert2',
#                                '. Ответ запишите в виде двоичного кода.']},
#             'answers': ['Ответ', 'insert3'],
#             'inserts': {'insert1': '228',
#                         'insert2': '322',
#                         'insert3': '550'}
#     }]
#     doc = []
#     tex = []
#     str = ''
#     flag = True
#
#     geometry_options = {"tmargin": "2cm", "lmargin": "2cm"}
#     for i in range(len(json_in)):
#         doc.append(Document(geometry_options=geometry_options))
#     fill_document(doc, json_in, flag)
#     for i in range(len(json_in)):
#         tex.append(doc[i].dumps())
#         tex[i] = r'\usepackage[english, russian]{babel}' + '\n' + tex[i]
#         str = modify_str(tex[i])
#         print(str)
#     with open('output.tex', 'w') as tex_out:
#         for line in tex:
#             tex_out.write(line)
#     #doc.generate_pdf('full', clean_tex=False)
