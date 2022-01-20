from macro import Macro
from individuo import Individuo
import matplotlib.pyplot as plt

"""
Class Povo:

    Estrutura do Povo do NSGA-II

    __init__()
        Método construtor da classe;

    criarGenes()
        Método de criar os genes dos Indivíduos;
        Da lista de genes obtido pelo Macro, os indivíduos recebem os alimentos aleatoriamente para cada categoria;

    criarPovo()
        Método de criar Povo do NSGA-II;
        Método mais robusto que criarGenes();

    size()
        Método que retornar o tamanho da população;

    extend()
        Método de extend do Povo
        Extende a lista de indivíduos;

    append()
        Método de append do Povo
        Adiciona mais indivíduos na lista de indivíduos;

    melhorIndividuo()
        Pega os melhores indivíduos, ou seja, pega os individuos da fronteira de Pareto;

    getIndividuo()
        Método que pega um indíviduo da lista de indivíduos;

"""

class Povo():
    def __init__(self, macro=None, log=None):
        self.individuos = []
        self.fronts = [[]]
        self.log = log
        self.extras = None
        self.filtro = None
        if macro is not None:
            self.genes = macro.getGenes()
            self.extras = macro.extra
            self.filtro = macro.filtro
    
    def criarGenes(self, categorias):
        cromossomo = []
        # lista de listas das categorias
        for c in categorias:
            cromossomo.append(self.taco.selectQuery(c))
        return cromossomo

    def criarPovo(self, tamanho):
        print("\nPovo::criarPovo\t Criando Povo ")
        for i in range(tamanho):
            if self.extras is not None and self.extras.fixar_alimentos:
                pessoa = Individuo(self.genes, self.filtro)
            else:
                pessoa = Individuo(self.genes)
            if self.log:
                print('[',i+1, '] ', end='')
                pessoa.printIndividuo()
            #pessoa = Individuo(random.choice(self.cereal[:tamanho]),random.choice(self.leite[:tamanho]), random.choice(self.fruta[:tamanho]))
            self.individuos.append(pessoa)

    def size(self):
        return len(self.individuos)
    
    def extend(self, novos_individuos):
        self.individuos.extend(novos_individuos)

    def append(self, novos_individuos):
        self.individuos.append(novos_individuos)

    def melhorIndividuo(self):
        melhorIndividuo = self.fronts[0]
        return melhorIndividuo

    def getIndividuo(self, index):
        return self.individuos[index]

    def setLog(self, log):
        self.log = log 


    def printPovo(self):
        for i in self.individuos:
            i.printIndividuo()

    def plotFronts(self, porcentagem):
        if porcentagem is not None and porcentagem != 0:
            percent = 'alimentos de {}g'.format(porcentagem)
        desempenho  = []
        dfront = []
        custo = []
        cfront = []
        for i in self.individuos:
            fitness = i.getFitness()
            desempenho.append(fitness[0])
            custo.append(fitness[1])
        for i in self.fronts[0]:
            fitness = i.getFitness()
            dfront.append(fitness[0])
            cfront.append(fitness[1])
        plt.plot(desempenho, custo, 'bo', dfront, cfront, 'ro')
        plt.title("NSGA-II com Gurobi - Problema da Dieta Alimentar "+percent)
        plt.xlabel('Desempenho (Menor é Melhor)')
        plt.ylabel(('Custo [R$] (Menor é Melhor)'))
        plt.show()