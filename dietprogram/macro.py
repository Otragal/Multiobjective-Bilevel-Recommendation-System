import database
import random

"""
Class Macro:

    It's the PACKAGE, so talked about in the dissertations...

    __init__()
        Class constructor method;

    inicizalizarGenes()
        Method that takes data from the categories of the Database;
        For each category, it stores an index of a self.gene list;

    construirCrossomoFixo()
        Filter method "fix feed";
        Get the desired category and put it in the index specified by the user;

    inicializarRestricao()
        Method that takes the constraints from the Database;
        The MAX and MIN constraints are stored in different lists;
        For each restriction an index is stored in the list;

"""

class Macro:
    def __init__(self, usu, obj, qtd_obj, categorias, des, macronutriente, fil, ex, nutricao, porcentagem, nutRestricao=None):
        self.taco = database.TacoDB()

        self.usuario = usu
        self.categoria = categorias

        self.desempenho = des
        self.macronutriente = macronutriente
        self.filtro = fil
        
        self.objetivos = obj
        self.qtd_objetivos = qtd_obj

        self.extra = ex    

        self.nutricao = nutricao
        self.porcentagem = porcentagem

        self.genes = []
        self.nutRestricao = []
        self.rMIN = []
        self.rMAX = []
        self.restricaoMIN = {}
        self.restricaoMAX = {}

        if nutRestricao is not None:
            self.nutRestricao = nutRestricao
            self.rMIN = [x + "MIN" for x in nutRestricao]
            self.rMAX = [x + "MAX" for x in nutRestricao]

        if self.extra.fixar_alimento:
            print('Macro::__init__\t Filtro "Fixar Alimentos" ativado')
            self.construirCrossomoFixo()
        else:
            print('Macro::__init__\t Filtro "Fixar Alimentos" desativado')

        
    def inicizalizarGenes(self):
        for c in self.categoria:
            self.genes.append(self.taco.selectCategoria(c, self.nutricao))
    
    # Creation of fixed food filters in the chromosome
    def construirCrossomoFixo(self):
        cromo = []
        codigo = []
        for index in range(self.filtro.tamanho):
            resultado = self.taco.selectOneFood(self.filtro.alimento[index], self.filtro.categoria[index], self.nutricao)
            codigo.append(resultado[1])
            cromo.append(resultado)
        self.filtro.setCromoxomo(cromo, codigo)
        print(self.filtro.cromoxomo)
        
        

    def inicializarRestricao(self):
        self.restricaoMIN = self.taco.selectConstrainMIN(self.usuario, self.rMIN)
        self.restricaoMAX = self.taco.selectConstrainMAX(self.usuario, self.rMAX)


# GET | SET Methods

    def getPessoaFromDB(self,comida, categoria):
        return self.taco.selectOneFood(comida, categoria)
    
    def getPessoa(self):
        return self.usuario.pessoa
    
    def getGenes(self):
        return self.genes

    def setRestricaoMIN(self, restricao):
        self.restricaoMIN = restricao
    
    def setRestricaoMAX(self, restricao):
        self.restricaoMAX = restricao

    def setPessoa(self, id):
        self.usuario.pessoa = id

    def quitProgram(self):
        self.taco.quit()
