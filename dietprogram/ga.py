from formatConverter import FormatConverter
from gurobyModel import GurobiModel
from fitnessGurobi import FitnessGurobi
from povo import Povo
from genetic import Genetic
from time import time

"""
Class GA()

    Aqui inicializa o algoritmo NSGA-II

    __init__()
        Preparação dos dados obtidos pelo usuário e banco de dados;
    
    iniciar()
        inicia o NSGA-II;

    resultados()
        mostra os resultados finais do NSGA-II;

"""

start = time()

class GA():
    def __init__(self, epocas, maxEpoca, maxPovo, macro, alter_condicoes=None, mais_condicoes=None, log=None):
        self.epocas = epocas
        self.maxEpoca = maxEpoca
        self.maxPovo = maxPovo
        self.macro = macro
        self.restricaoMIN = FormatConverter.makeDictNutrition(self.macro.nutRestricao, self.macro.restricaoMIN)
        self.restricaoMAX = FormatConverter.makeDictNutrition(self.macro.nutRestricao, self.macro.restricaoMAX)
        
        
        self.log = log
        self.model_name = 'modelo_'+str(macro.usuario.pessoa)
        self.model = GurobiModel.createModel(self.model_name)
        self.povo = Povo(macro=self.macro)
        # Cria o Primeiro Povo
        self.povo.criarPovo(tamanho=self.maxPovo)
        self.resultado = None
        if mais_condicoes is not None:
            for cond in mais_condicoes:
                FormatConverter.addOneDictNutrition(cond[0],cond[1],self.restricaoMIN)
                FormatConverter.addOneDictNutrition(cond[2],cond[3],self.restricaoMAX)
        #print(self.restricaoMAX)
        #input("Press Enter to continue...")

    def iniciar(self):
        # Define os fitness dos individuos
        
        print('GA::iniciar\t Definindo o Fitness dos Indivíduos...')
        self.povo = FitnessGurobi.setFitnessPovo(self.macro, self.model, self.model_name, self.povo)
        print("GA::iniciar\t Inicializando o Povo na EPOCA: %s" % (self.epocas))
        #self.povo.getIndividuo(1).printIndividuoAll()
        input("Press Enter to continue...")                                                                        
        while self.epocas < self.maxEpoca:
            self.epocas += 1
            print("\n\t Evoluindo Povo para EPOCA: %s" %(self.epocas))
            self.povo, self.resultado = Genetic.evoluir_NSGA(self.povo, self.macro, self.maxPovo, self.model, self.model_name, self.log)
            #self.povo.printPovo()
            input("Press Enter to continue...")
            print()

        self.resultados()
       # melhorIndividuo = self.resultado.melhorIndividuo()

        #print("GA::iniciar\t Melhor Individuo Encontrado")
       
        
        #for ind in melhorIndividuo:
        #    ind.printIndividuo()
        
        #self.resultado.plotFronts()

    def resultados(self):
        melhorIndividuo = self.resultado.melhorIndividuo()
        print("GA::resultados\t Apresentando os resultados")
        print("CATEGORIAS\t", end='')
        for cat in self.macro.categoria:
            print(cat, '\t', end='')
        print('OBJETIVOS\n')
        for key, value in enumerate(melhorIndividuo):
            print("OPÇÃO ",key,"\t",end='')
            value.printIndividuo()
        print('\n')

        self.resultado.plotFronts(self.macro.porcentagem)
        

