import json
import numpy as np

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat
from pylatex.utils import italic
import os

def fill_document(doc, json_in, flag):

    for i in range(len(json_in['text'])-1):
        doc.append(json_in['text'][i] + ' ')
        doc.append(json_in['inserts'][i] + ' ')
    doc.append(json_in['text'][-1] + ' ')

    if flag:
        doc.append('\nОтвет:\n')
        for ans in json_in['answers']:
            doc.append(ans + ' ')
    return

if __name__ == '__main__':
    json_in = {}
    with open('petuchi.json', 'r') as data_file:
        json_in = json.load(data_file)
    print(json_in)
    flag = False

    image_filename = os.path.join(os.path.dirname(__file__), 'kitten.jpg')

    geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
    doc = Document(geometry_options=geometry_options)
    fill_document(doc, json_in, flag)

    tex = doc.dumps()
    print(tex)
    with open('output.tex', 'w') as tex_out:
        for line in tex:
            tex_out.write(line)
    #doc.generate_pdf('full', clean_tex=False)
