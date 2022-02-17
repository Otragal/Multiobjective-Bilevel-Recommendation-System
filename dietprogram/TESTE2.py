"""
    MULTI-OBJETIVO
        Vi que o multi-objetivo precisa de vários funções objetivas
    Então, eu preciso realizar várias opçõies de gorubi, e eu preciso encontrar os pesos que definem a importancia de cada multiobjetivo.
    Com esses pesos, eu posso utilizar para a definição de seleção de melhores individvódips no algirtmo NSGA-III, e isso benecifiará 
    a escolha do melhor individuo.

    Então, vendo isso, se terá mais de uma função objetivo, eu preciso cirar vários modelos de gurobi.
    Sendo que a primeira função objetivo seria:
        ENERGIA, o total de nergia a ser consumida, veja bem, nisso não tenho que colocar a restrição de energia
        FIBRA ALIMENTAR: poxa é bem importante a fibra, então eu posso colocar restrição energia e tirar a a restrição fibra
        PROTEINA: sim, é bom, então pode ser um função objetivo.

    Então, se terei 3 gurobis, pelo menos isso, eu preciso separar as restrições, né?
    Porque se aplicar as mesmas restrições para todas, terei soluções parecidas, o que vai causar uma solução unica.
    Então eu preciso separar as restrições.
    Tipo, Energia ta relacionado com os nuutrientes, tipo, vitaminas
    Fibra alimentar, ta relacionado com o calcio, ferro, né?
    PROTEINA: ta relacionado com os demais
    
"""


"""
    Na verdade não é legal colocar tudo de uma vez só
    Os principais nutrientes são:
        1. Carboidratos
            - Energia
            - Fibra Aliemntar
            - Açucar
        2. Proteina
        3. Sais Minerais
            - Calcio
            - Cloro
            - Cobre
            - Fluor
            - Ferro
            - Magnesio
            - Fosfor
            - Sodio
            - Zinco
        4. Vitaminas
            - A, B,C, E etc
        
        Ideia interessnate:
            Fazer um Gurobi para Energia, Fibra ALimenta e Proteina
            Fazer um segundo gurobi para Sais Minerais
            Fazer um terceiro Gurobi para Vitaminas?

            Ai eu faço o segundo, os 3 gurobis vão fazer a quantidade, soma todos e fazem a média
            Esta média de quantidade dos 3 será avaliado pela quantidade dos alimentos e proporção
"""

import matplotlib.pyplot as plt
import math
from collections import defaultdict

class Testes:

    def plot_graph():
        peso = []
        qtd = []
        maxe = []
        intervalo = [900, 2100]
        inter = [math.floor(intervalo[0]/2),intervalo[0], intervalo[1], math.floor(intervalo[1]*(1+0.5)), intervalo[1]*2]
        zero = [0]*intervalo[1]*2
        for i in range(0,inter[4],1):
            if i == 0:
                peso.append(-1)
            if i >= 0 and i <= inter[0]:
                peso.append(-(inter[0]-i)/inter[0]) 

            if i > inter[0] and i < inter[1]:
                peso.append((i-inter[0])/(inter[1]-inter[0]))

            if i >= inter[1] and i <= inter[2]:
                peso.append(1)

            if i > inter[2] and i <= inter[3]:
                peso.append((inter[3]-i)/(inter[3]-inter[2]))

            if i > inter[3] and i < inter[4]:
                peso.append(-(i-inter[3])/(inter[4]-inter[3]))
            if i >= inter[4]:
                peso.append(-1)

        plt.plot(peso)
        plt.plot(zero,'r--')
        #plt.plot(qtd,peso)
        #plt.plot(qtd,zero, 'black')
        #plt.plot(qtd,maxe,'r--')
        plt.plot(900,1,'ro')
        plt.plot(2100,1,'ro')
        plt.plot(inter[0],0,'ro--')
        plt.plot(inter[3],0, 'ro--')
        plt.annotate('{}g'.format(inter[0]), xy=(inter[0],0), xytext=(inter[0]-300,0.05))
        plt.annotate('{}g'.format(inter[3]),xy=(inter[3],0),xytext=(inter[3]+100,0.05))
        plt.annotate('900g', xy=(900,1), xytext=(450,0.95))
        plt.annotate('2100g',xy=(2100,1),xytext=(2200,0.95))
        #plt.annotate('Nota 0.9',xy=(1000,0.9),xytext=(1000,0.95))
        plt.title("Formula do Peso")
        plt.xlabel('Peso (gramas)')
        plt.ylabel(('Peso(x)'))
        plt.show()

    def find_duplication(codigo):
        duplicada = []
        d = defaultdict(list)
        for i,item in enumerate(codigo):
            d[item].append(i)

        for k,v in d.items():
            if len(v)>1:
                duplicada.extend(v)

        dupla = [v for k,v in d.items() if len(v)>1]
        
        return duplicada, dupla

ca = ['cereais', 'carnes', 'carnes', 'leguminosas', 'leguminosas', 'verduras', 'cereais','carnes','ovos', 'leguminosas','verduras','verduras']
duplicada, duplas = Testes.find_duplication(ca)
conjunto = set(ca)
print(duplicada)
print(duplas)
print(conjunto)