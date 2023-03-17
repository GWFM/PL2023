import re
import sys

valid_coins = ['10c', '20c', '50c', '1e', '2e']

def peakUp():
    print('----Bem-vindo(a) à Cabine Telefónica----')
    print('Para utilizar o serviço, insira uma quantia desejada em moedas!')

def coins(line,saldo):
    recived_coins = re.findall(r'\d+[c,e]', line)
    for coin in recived_coins:
        if coin in valid_coins:
            if coin == '10c':
                saldo += 0.1
            elif coin == '20c':
                saldo += 0.2
            elif coin == '50c':
                saldo += 0.5
            elif coin == '1e':
                saldo += 1
            elif coin == '2e':
                saldo += 2
        else:
            print(f'{coin} não é uma moeda válida!')
    print(f'O seu saldo é de: {saldo} €')
    return saldo

def turnOff(saldo):
    print('A desligar a Cabine Telefónica...')
    print(f'O seu troco é de: {saldo} €')
    sys.exit(0)

def call(line,saldo):
    number = re.sub(r'T=', '', line)
    if re.match(r'601|641',number):
        print('Este número não é permitido neste telefone. Queira discar novo número!')
    elif re.match(r'00',number):
        if saldo >= 1.5:
            print(f'Chamada efetuada para o número {number}')
            saldo -= 1.5
            print(f'O seu saldo é de: {saldo} €')
        else:
            print('Saldo insuficiente!')
    elif re.match(r'800',number) and len(number) == 9:
        print(f'Chamda efetuada para o número {number}')
        print(f'O seu saldo é de: {saldo} €')
    elif re.match(r'808',number) and len(number) == 9:
        if saldo >= 0.1:
            print(f'Chamda efetuada para o número {number}')
            saldo -= 0.1
            print(f'O seu saldo é de: {saldo} €')
        else:
            print('Saldo insuficiente!')
    elif re.match(r'2',number) and len(number) == 9:
        if saldo >= 0.25:
            print(f'Chamda efetuada para o número {number}')
            saldo -= 0.25
            print(f'O seu saldo é de: {saldo} €')
        else:
            print('Saldo insuficiente!')
    else:
        print('Número inválido. Queira discar novo número!')
    return saldo



def cancel(saldo):
    print('Serviço cancelado!')
    print(f'O seu troco é de: {saldo} €')
    sys.exit(0)

def main():
    saldo = 0
    for line in sys.stdin:
        line = line.strip()
        if re.match(r'LEVANTAR', line):
            peakUp()
        elif re.match(r'MOEDA', line):
            saldo = coins(line,saldo)
        elif re.match(r'T=', line):
            saldo = call(line,saldo)
        elif re.match(r'POUSAR', line):
            turnOff(saldo)
        elif re.match(r'ABORTAR', line):
            cancel(saldo)
        else:
            print('ERRO')

if __name__ == '__main__':
    main()