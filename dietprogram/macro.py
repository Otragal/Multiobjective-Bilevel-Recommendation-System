import database
import random

"""
Class Macro:

    É o PACOTE, tão falado nas dissertações...

    __init__()
        Método construtor da classe;

    inicizalizarGenes()
        Método que pega os dados das categorias do Banco de Dados;
        Para cada categoria, ele armazena em um indice de uma lista self.gene;

    construirCrossomoFixo()
        Método do filtro "fixar aliemento"
        Pega a categoria desejada e coloque no indice especificado pelo usuário;

    inicializarRestricao()
        Método que pega as restrições do Banco de Dados;
        As restrições MAX e MIN são armazenados em listas diferentes;
        Para cada restrição é armazenado em um indice da lista;

"""

class Macro:
    def __init__(self, usu, categorias, des, fil, ex, nutricao, porcentagem, nutRestricao=None):
        self.taco = database.TacoDB()

        self.usuario = usu
        self.categoria = categorias

        self.desempenho = des
        self.filtro = fil

        self.extra = ex    
        #self.tam_categoria = tam_categoria
        #self.energia_refeicao = energia_refeicao
        #self.quantidade_refeicao = quantidade_refeicao
        #self.peso_refeicao = peso_refeicao

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

        if self.extra.fixar_alimentos:
            self.construirCrossomoFixo()
        else:
            print('Macro::__init__\t Sem fixar alimentos')

    # MÉTODO ANTIGO
    #def definirGenes(self):
    #    # Cromossomo = Cereal, Leite, Fruta, Vegetal, Carne, Fruta, Cereal,Leite, Fruta]
    #    self.genes.append(self.selectCategoria('cereais', self.nutricao))
    #    self.genes.append(self.selectCategoria('leites', self.nutricao))
    #    self.genes.append(self.selectCategoria('frutas', self.nutricao))
    #    if random.random() <= 0.5:
    #        self.genes.append(self.selectCategoria('verduras', self.nutricao))
    #    else:
    #        self.genes.append(self.selectCategoria('leguminosas', self.nutricao))
    #    if random.random() <= 0.5:
    #        self.genes.append(self.selectCategoria('carnes', self.nutricao))
    #    else:
    #        self.genes.append(self.selectCategoria('pescados', self.nutricao))
    #    self.genes.append(self.selectCategoria('cereais', self.nutricao))
    #    self.genes.append(self.selectCategoria('leites', self.nutricao))
    #    self.genes.append(self.selectCategoria('frutas', self.nutricao))

        
    def inicizalizarGenes(self):
        for c in self.categoria:
            self.genes.append(self.taco.selectCategoria(c, self.nutricao))
    
    # criação de filtros de comidas fixas no cromosso
    def construirCrossomoFixo(self):
        cromo = []
        for index in range(self.filtro.tamanho):
            cromo.append(self.taco.selectOneFood(self.filtro.alimento[index], self.filtro.categoria[index], self.nutricao))
        self.filtro.setCromoxomo(cromo)
        print(self.filtro.cromoxomo)
        
        

    def inicializarRestricao(self):
        self.restricaoMIN = self.taco.selectConstrainMIN(self.usuario, self.rMIN)
        self.restricaoMAX = self.taco.selectConstrainMAX(self.usuario, self.rMAX)


# MÉTODOS GET | SET

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
