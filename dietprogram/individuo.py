import random


"""
Class Individuo:
    
    Estrutura do Indivíduo do NSGA-II

    __init__()
        Construtor da classe
    
    generateGene()
        Método de gerar os genes do indivíduo ao pegar os dados presentes do Macro;

    fixComida()
        Método do filtro "fixar a comida" para que o NSGA-II não possa alterar este alimento;

    dominates()
        Método de verificar se o indivíduo A domina o indivíduo B;

    size()
        Método de retornar o tamanho do cromosso do Indivíduo;

"""


class Individuo():
    def __init__(self, genes=None, filtro=None):
        self.codigo = []
        self.cromossomo = []
        self.atributos = None
        self.fitness = None
        # NSGA-II
        self.domination_count = None
        self.dominated_solutions = None
        self.crowding_distante= None
        self.rank = None
        if genes is not None:
            self.generateGene(genes)
        if filtro is not None:
            self.fixComida(filtro)

    def generateGene(self, genes):
        for g in genes:
            #print(g)
            combina = random.choice(g[:]) #tuplas
            #print(combina)
            self.codigo.append(combina[1])
            self.cromossomo.append(combina)

    def fixComida(self, filtro):
        for i in range(filtro.tamanho):
            self.cromossomo[filtro.indice[i]] = filtro.cromoxomo[i]
        

    #NSGA
    def dominates(self, outro):
        # Se A domina  B quando:
        andC = True
        orC = False
        for first, second in zip(self.fitness, outro.fitness):
            # Cond_E = Ax <= Bx E Ay <= By
            andC = andC and first <= second
            # Cond_OU = Ax <= Bx OU Ay < By
            orC = orC or first < second
        # Cond_E E Cond_OU
        return (andC and orC)

    def size(self):
        return len(self.cromossomo)

# MÉTODOS DE SET | GET

    def getFitness(self):
        return self.fitness
    
    def setFitness(self, fit):
        self.atributos = fit.pop(1)
        self.fitness = fit.pop(0)
        print(self.fitness)

    def getGene(self, index):
        return self.cromossomo[index]

    def setGene(self, index, gene):
        self.cromossomo[index] = gene

    def applyGene(self,gene):
        self.cromossomo.append(gene)

    def getCategoria(self, c):
        if hasattr(self, c):
            return getattr(self ,c)
        else:
            print('Individuo::getCategoria\t Não existe atributo {}'.format(c))
            return None

    def setCategoria(self, c, alimento):
        if hasattr(self, c):
            setattr(self, c, alimento)
        else:
            print('Individuo::setCategoria\t Não existe atributo {}'.format(c))

# MÉTODOS DE PRINT

    def printIndividuoAll(self):
        print(self.cromossomo, " ", self.fitness, '\n')

    def printIndividuo(self):
        for gene in self.cromossomo:
            print(gene[0].split(', ',1)[0], '\t', end= '')
        print(self.fitness, '\n')
        for key, value in enumerate(self.atributos):
            print("ATRIBUTO ",key,"\t", end='')
            for v in value:
                print("%.2f" % v,'\t',end='')
            print('\n')
        