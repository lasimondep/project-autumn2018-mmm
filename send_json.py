import json

text = ''
json_dict = {'text' : [], 'answers': [], 'inserts' : []}
flag = ''
with open('input.txt', 'r') as fin:
    for line in fin:
        if line.strip() == 'text':
            flag = line.strip()
            continue
        if line.strip() == 'answers':
            flag = line.strip()
            continue
        if line.strip() == 'inserts':
            flag = line.strip()
            continue
        if flag == 'text':
            json_dict['text'] += [line.strip()]
        if flag == 'answers':
            json_dict['answers'] += [line.strip()]
        if flag == 'inserts':
            json_dict['inserts'] += [line.strip()]

print(json_dict)
with open('petuchi.json', 'w') as jout:
    json.dump(json_dict, jout)