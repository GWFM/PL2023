import json

def parseFile():
    dic = {}
    with open("processos.txt", "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            if line == '':
                continue
            line = line.split('::')
            dic[line[0]] = {'date':[line[1].split('-')[0],line[1].split('-')[1],line[1].split('-')[2]], 'name': line[2], 'father': line[3], 'mother': line[4], 'family': filterFam(line[5])}
    return dic

def filterFam(fam):
    res = []
    fam = fam.split('.')
    if fam == ['']:
        return res
    elif len(fam)>=4 and fam[-3]==' Proc':
            res.append({'name':fam[-4].split(',')[:-1], 'member':fam[-4].split(',')[-1], 'proc':fam[-2]})
    return res

def yearFrequency(dic):
    dist = DistributionTable('Year Frequency')
    dic2 = {}
    total = 0
    for key in dic:
        if dic[key]['date'][0] in dic2:
            dic2[dic[key]['date'][0]] += 1
        else:
            dic2[dic[key]['date'][0]] = 1
        total += 1
    
    for key in dic2:
        dist.add(key, dic2[key]/total)
    print(dist)

def fstNameBySec(dic):
    dist = DistributionTable('Name by Sec')
    dic2 = {}
    for key in dic:
        sec=str(int(dic[key]['date'][0][:2])+1)
        names=dic[key]['name'].split(' ')
        fstName=names[0]
        if sec in dic2:
            if fstName in dic2[sec]:
                dic2[sec][fstName] += 1
            else:
                dic2[sec][fstName] = 1
        else:
            dic2[sec] = {fstName: 1}

    for key in dic2:
        for key2 in dic2[key]:
            dic2[key][key2]=dic2[key][key2]/sum(dic2[key].values())

    for key in dic2:
        dic2[key] = dict(sorted(dic2[key].items(), key=lambda item: item[1], reverse=True))
        i = 0
        for key2,value in dic2[key].items():
            if i < 5:
                dist.add(key, key2 + ' ' + str(value) + '\n')
                i += 1
            else:
                continue

    print(dist)

def lstNameBySec(dic):
    dist = DistributionTable('Name by Sec')
    dic2 = {}
    for key in dic:
        sec=str(int(dic[key]['date'][0][:2])+1)
        names=dic[key]['name'].split(' ')
        lstName=names[-1]
        if sec in dic2:
            if lstName in dic2[sec]:
                dic2[sec][lstName] += 1
            else:
                dic2[sec][lstName] = 1
        else:
            dic2[sec] = {lstName: 1}

    for key in dic2:
        for key2 in dic2[key]:
            dic2[key][key2]=dic2[key][key2]/sum(dic2[key].values())

    for key in dic2:
        dic2[key] = dict(sorted(dic2[key].items(), key=lambda item: item[1], reverse=True))
        i = 0
        for key2,value in dic2[key].items():
            if i < 5:
                dist.add(key, key2 + ' ' + str(value) + '\n')
                i += 1
            else:
                continue

    print(dist)

def relationFreq(dic):
    dist = DistributionTable('Relation Frequency')
    dic2 = {}
    for key in dic:
        for rel in dic[key]['family']:
            if rel['member'] in dic2:
                dic2[rel['member']] += 1
            else:
                dic2[rel['member']] = 1
    for key in dic2:
        dist.add(key, dic2[key]/sum(dic2.values()))
    print(dist)

def outputJson(dic):
    dic2 = {}
    aux = 1
    for key in dic:
        if aux<21:
            dic2[aux] = {'regist': key ,'date': dic[key]['date'], 'name': dic[key]['name'], 'father': dic[key]['father'], 'mother': dic[key]['mother'], 'family': dic[key]['family']}
            aux += 1
        else:
            break

    with open('registos.json', 'w') as f:
        f.write(json.dumps(dic2, indent=4))

def main():
    dic = parseFile()
    #yearFrequency(dic)
    #nameBySec(dic)
    #lstNameBySec(dic)
    #relationFreq(dic)
    outputJson(dic)

class DistributionTable:
    def __init__(self, name):
        self.name = name
        self.table = {}
    
    def add(self, key, value):
        if key in self.table:
            self.table[key] += value
        else:
            self.table[key] = value
    
    def __str__(self):
        printer = dict(sorted(self.table.items()))
        s = '----------' + self.name + '----------\n'
        for key in printer:
            s += str(key) + ': ' + str(printer[key]) + '\n'
        s += '----------------------------------'
        return s

if __name__ == "__main__":
    main()
