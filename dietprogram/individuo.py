import random


"""
Class Individuo:
    
    NSGA-II Structure of the Individual

    __init__()
        class constructor
    
    generateGene()
        Method of generating the individual's genes by taking the data present from the Macro;

    fixComida()
        "Fix the food" filter method so that the NSGA-II cannot change this food;

    dominates()
        Method of verifying whether individual A dominates individual B;

    size()
        Method of returning the size of the Individual's chromosome;

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
        if filtro is not None and filtro is True:
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
        

    #NSGA - dominates
    def dominates(self, outro):
        # If A dominates B when:
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
        self.codigo[index] = gene[1]
        self.cromossomo[index] = gene

    def applyGene(self,gene):
        self.codigo.append(gene[1])
        self.cromossomo.append(gene)

    def getCategoria(self, c):
        if hasattr(self, c):
            return getattr(self ,c)
        else:
            print('Individuo::getCategoria\t There is no attribute {}'.format(c))
            return None

    def setCategoria(self, c, alimento):
        if hasattr(self, c):
            setattr(self, c, alimento)
        else:
            print('Individuo::setCategoria\t There is no attribute {}'.format(c))

# MÉTODOS DE PRINT

    def printIndividuoAll(self):
        print(self.cromossomo, " ", self.fitness, '\n')

    def printIndividuo(self):
        for gene in self.cromossomo:
            print(gene[0].split(', ',1)[0], '\t', end= '')
        print(self.fitness, '\n')
        for key, value in enumerate(self.atributos):
            print("ATTRIBUTE ",key,"\t", end='')
            for v in value:
                print("%.2f" % v,'\t',end='')
            print('\n')
        