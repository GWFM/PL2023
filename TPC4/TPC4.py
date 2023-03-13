import json
import re

def fields(line):
    header = re.finditer(r'([aA-zZ])(\w)+([a-z]|((\{\d,\d\}|\{\d\})(::[a-z]+)?))',line)
    obj = {}
    header_fields = []
    for i in header:
        header_fields.append(i.group())
    for i in header_fields:
        if re.search(r'\{\d,\d\}', i):
            #in camp name, remove the {min,max} part and if there is ::type, remove it too
            obj[i] = {'type': 'minmax', 'name' : re.sub(r'::[a-z]*','',(re.sub(r'\{\d,\d\}', '', i))), 'min': int(re.search(r'\d+', re.search(r'\{\d,\d\}', i).group()).group()), 'max': int(re.search(r'\d+', re.search(r',\d+\}', i).group()).group()), 'extra': {}}
        elif re.search(r'\{\d\}', i):
            obj[i] = {'type': 'number', 'name' : re.sub(r'::[a-z]*','',(re.sub(r'\{\d\}', '', i))), 'size': int(re.search(r'\d+', re.search(r'\{\d\}', i).group()).group()), 'extra': {}}
        else :
            obj[i] = {'type': 'normal', 'name' : i, 'extra': {}}
        if re.search(r'::[a-z]+', i):
           obj[i]['extra']['type'] = re.search(r'::[a-z]+', i).group()
           obj[i]['extra']['values'] = []
    return fields

def parse_line(line, header):
    obj = {}
    line = re.split(r',', line)
    max = len(line)
    i=0
    while i < max:
        if header[i]['type'] == 'normal':
            obj[header[i]['name']] = line[i]
        elif header[i]['type'] == 'number':
            obj[header[i]['name']] = []
            for j in range(header[i]['size']):
                obj[header[i]['name']].append(int(line[i+j]))
            i += header[i]['size'] - 1
        elif header[i]['type'] == 'minmax':
            obj[header[i]['name']] = []
            for j in range(header[i]['min'], header[i]['max']+1):
                obj[header[i]['name']].append(int(line[i+j]))
            i += header[i]['max'] - header[i]['min'] + 1
        if 'type' in header[i]['extra']:
            if header[i]['extra']['type'] == '::sum':
                obj[header[i]['name'+header[i]['extra']['type']]] = sum(header[i]['extra']['values'][int(obj[header[i]['name']])] )
            elif header[i]['extra']['type'] == '::media':
                obj[header[i]['name'+header[i]['extra']['type']]] = sum(header[i]['extra']['values'][int(obj[header[i]['name']])])/len(header[i]['extra']['values'][int(obj[header[i]['name']])] )
        i += 1 
    return obj

def write_json(filename='alunos.csv'):
    dic = []
    with open(filename, 'r') as f:
        header = fields(f.readline())
        for line in f:
            dic.append(parse_line(line, header))
    with open('alunos.json', 'w') as f:
         f.write(json.dumps(dic, indent=4, ensure_ascii=False))

        

def main():
    write_json()



if __name__ == '__main__':
    main()