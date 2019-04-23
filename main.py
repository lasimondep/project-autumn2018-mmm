import json
import re
import os

from pylatex import *

from common import AMQP_client


def modify_str(str1, Type):
    pattern1 = r'insert\d{,100}'
    str1 = str1.replace('%', '')
    str1 = str1.replace(r'\normalsize', '')
    str1 = str1.replace(r'\newline', '\n')
    str1_list = str1.split()
    interface_str = ''
    flag = False

    if Type == "get_task_text":
        temp_str = ''
        interface_str = []
        for i in str1_list:
            if i == '\\begin{document}':
                flag = True
                continue
            if flag:
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
    if Type == "get_pdf" or Type == "post_task":
        for i in str1_list:
            if i == '\\begin{document}':
                flag = True
                continue
            if flag:
                if i == '\\end{document}':
                    break
                interface_str += i + ' '
    return interface_str


def func(data, Type):
    json_in = data
    flag = True
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
        tex = doc.dumps()
    elif Type == 'get_task_text':
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

    for i in range(len(json_in)):
        for key in json_in[i]['text']:
            match = re.fullmatch(pattern2, key)
            if match:
                for text in json_in[i]['text'][key]:
                    match1 = re.findall(pattern1, text)
                    if match1:
                        doc[i].append(json_in[i]['inserts'][text]+ text)
                    else:
                        doc[i].append(text + ' ')
    return


def pdf_generate(doc, json_in, flag):
    pattern1 = r'insert\d{,100}'
    pattern2 = r'text\d{,100}'
    pattern3 = r'table\d{,100}'
    pattern4 = r'row\d{,100}'
    pattern5 = r'col\d{,100}'

    for i in range(len(json_in)):
        doc.append('\n\tЗадача' + str(i+1) + ':\n')
        for key in json_in[i]['text']:
            match = re.fullmatch(pattern2, key)
            if match:
                for text in json_in[i]['text'][key]:
                    match1 = re.findall(pattern1, text)
                    if match1:
                        doc.append(json_in[i]['inserts'][text] + ' ')
                    else:
                        doc.append(text + ' ')

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

    for i in range(len(json_in)):
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
            json_tex = func(Data, Type)
            json_tex = json.dumps(json_tex)
            self.send('interface', Id, 'get_pdf', json_tex)

        if Type == "get_task_text":
            json_text = []
            for i in range(len(Data)):
                json_text.append(json.loads(Data[i]))
            tex_lst = func(json_text, Type)
            json_out = json.dumps(tex_lst)
            self.send('interface', Id, 'tex_task_text', json_out)


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
#     json_text = [{
#         'text': {'text1': ['Сложите число', 'insert1', 'с числом', 'insert2', '. Ответ запишите в виде двоичного кода.']},
#         'answers': ['Ответ', 'insert3'],
#         'inserts': {'insert1': '322',
#                     'insert2': '228',
#                     'insert3': '550'}}, {
#         'text': {'text1': ['Сложите число', 'insert1', 'с числом', 'insert2', '. Ответ запишите в виде двоичного кода.']},
#         'answers': ['Ответ', 'insert3'],
#         'inserts': {'insert1': '228',
#                     'insert2': '322',
#                     'insert3': '550'}
#     }]
#     tex = []
#     flag = True
#     Type = "get_task_text"
#
#     tex_lst = func(json_text, Type)
#     json_out = json.dumps(tex_lst)
#
#     print(tex_lst)
#
#     for i in tex_lst:
#         print(i)
#
#     with open('output.tex', 'w') as tex_out:
#         for i in tex_lst:
#             for line in i:
#                 tex_out.write(line)
#                 tex_out.write('\n')
