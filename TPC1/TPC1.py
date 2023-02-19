import csv

def main():
    options = input('Que distribuição deseja?\n 1 - Distribuição de sexo\n 2 - Distribuição de grupos de idade\n 3 - Distribuição de colesterol\n 4 - Todas\n ')
    age_groups = [(30,34), (35,39), (40,44), (45,49), (50,54), (55,59), (60,64), (65,69), (70,74), (75,79)]
    info = read_file('myheart.csv')
    if options == '1':
        sex_desiase_distribution(info)
    elif options == '2':
        age_groups_distribution(info, age_groups)
    elif options == '3':
        colesterol_distribution(info)
    elif options == '4':
        sex_desiase_distribution(info)
        age_groups_distribution(info, age_groups)
        colesterol_distribution(info)


def read_file(filename):
    info = []
    with open(filename) as f:
        lines = csv.reader(f)
        for line in lines:
            info.append(line)
    info.pop(0)
    info.pop(1)
    return info

def sex_desiase_distribution(info):
    dist = DistributionTable('Sex Distribution')
    male = 0
    female = 0
    total = 0
    for line in info:
        if line[5] == '1':
            total += 1
            if line[1] == 'M':
                male += 1
            else:
                female += 1
    dist.add('Male',(male/total))
    dist.add('Female',(female/total))
    print(dist)

def age_groups_distribution(info, age_groups):
    dist = DistributionTable('Age Groups Distribution')
    for age in age_groups:
        total = 0
        amount = 0
        for line in info:
            if line[5] == '1':
                total += 1
                if age[0] <= int(line[0]) <= age[1]:
                    amount += 1
        dist.add(str(age[0]) + '-' + str(age[1]), (amount/total))
    print(dist)

def colesterol_distribution(info):
    dist = DistributionTable('Colesterol Distribution')
    total = 0
    ranges = {}
    for line in info:
        if line[5] == '1':
            total += 1
            if int(line[3]) in ranges:
                ranges[int(line[3])] += 1
            else:
                ranges[int(line[3])] = 1
    analized = []
    for key in ranges:
        if key in analized:
            continue
        rangelist = range(key,key+10)
        range_amount = 0
        for i in rangelist:
            if i in ranges:
                range_amount += ranges[i]
                analized.append(i)
        dist.add(str(key) + '-' + str(key+9), (range_amount/total))
    print(dist)

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
        s = '----------' + self.name + '----------\n'
        for key in self.table:
            s += str(key) + ': ' + str(self.table[key]) + '\n'
        s += '----------------------------------'
        return s
        
        

if __name__ == '__main__':
    main()

