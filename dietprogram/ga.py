from formatConverter import FormatConverter
from gurobyModel import GurobiModel
from fitnessGurobi import FitnessGurobi
from povo import Povo
from genetic import Genetic
from results import Results

from time import time

"""
Class GA()

    Here initializes the NSGA-II algorithm;

    __init__()
        Preparation of data obtained by the user and database;
    
    iniciar()
        Starts NSGA-II;

    resultados()
        Shows the final results of the NSGA-II;

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
        if log:
            print('GA::__init__\t Constrains MIN e Max')
            print(self.macro.nutRestricao)
            print(self.restricaoMIN)
            print(self.restricaoMAX)
            print('Amount of Food: ', len(macro.categoria))
            print(macro.categoria)
            input("Press Enter to continue...")
            print()
        
        self.log = log
        self.model_name = 'modelo_'+str(macro.usuario.pessoa)
        self.model = GurobiModel.createModel(self.model_name)
        self.povo = Povo(macro=self.macro)
        # Creates First Population
        self.povo.criarPovo(tamanho=self.maxPovo)
        self.resultado = None
        if mais_condicoes is not None:
            for cond in mais_condicoes:
                FormatConverter.addOneDictNutrition(cond[0],cond[1],self.restricaoMIN)
                FormatConverter.addOneDictNutrition(cond[2],cond[3],self.restricaoMAX)


    def iniciar(self):
        # Defines the fitness of individuals
        print('GA::iniciar\t Building a First Population...')
        self.povo = FitnessGurobi.setFitnessPovo(self.macro, self.model, self.model_name, self.povo)
        print("GA::iniciar\t Starting Povo in Epoch: %s" % (self.epocas))
        input("Press Enter to continue...")                                                                        
        while self.epocas < self.maxEpoca:
            self.epocas += 1
            print("\n\t Evolving People for Epoch: %s" %(self.epocas))
            self.povo, self.resultado = Genetic.evoluir_NSGA(self.povo, self.macro, self.maxPovo, self.model, self.model_name, self.log)
            print()

        self.resultados()


    def resultados(self):
        fronteira = self.resultado.getFront()
        print("GA::resultados\t Presenting the results")
        print("CATEGORIAS\t", end='')
        for cat in self.macro.categoria:
            print(cat, '\t', end='')
        print('OBJETIVOS\n')
        for key, value in enumerate(fronteira):
            print("OPÇÃO ",key,"\t",end='')
            value.printIndividuo()
        print('\n')

        Results().createFrontsCSV(self.resultado, self.macro)
        
        # Others methods to plot graphs
        
        #Results().plotFronts(self.resultado, self.macro)
        #Results().plotFrontsIntakes(self.resultado, self.macro)
        #Results().plotFrontFoods(self.resultado, self.macro)
        #Results().boxSplotMacronutrientes(self.resultado, self.macro)
        #Results().stackBarEnergyMacro(self.resultado, self.macro)
        #self.resultado.plotFronts(self.macro.porcentagem)
        #self.resultado.plotFrontsIntakes(self.macro, self.macro.porcentagem)
        #self.resultado.plotFrontFoods(self.macro)
        #self.resultado.boxSplotMacronutrientes(self.macro)
        #self.resultado.stackBarEnergyMacro(self.macro)