import os
from macro import Macro
from ga import GA
import database
from filtros import comida, desempenho, usuario, extras, macronutriente

class App():
    
    
    def __init__(self):
        print("Iniciando...\n")

        epocas = 0
        maxEpoca = 8 # maxEpoca = 10 : Concentração de mesmos alimentos alto
        maxPovo = 100 #Default: 100

        pessoa = 3
        idade = 25
        porcentagem = 10

        usu = usuario(pessoa, idade, porcentagem)

        #Objetivos
        #objetivos = ['Energia1', 'Preco']
        qtd_objetivos = 2
        objetivos = ['Energia1', 'Preco']

    
    # Cardápio Diário:
        # Café da Manhã
        ca = ['cereais', 'leites', 'frutas']
        #ca = ['cereais', 'carnes', 'carnes', 'leguminosas', 'leguminosas', 'verduras']
        # Almoço
        al = ['cereais', 'leguminosas', 'verduras', 'carnes', 'ovos']
        #al = ['cereais','carnes','ovos', 'leguminosas','verduras','verduras']
        # Jantar
        ja = ['bebidas', 'verduras', 'pescados', 'leites']
        #ja = ['cereais', 'pescados','ovos', 'verduras', 'verduras']
        # Lanche
        la = ['verduras', 'gorduras', 'frutas']

        # Criação do Vetor Unitário:
        # Vetor
        #categorias = ca + al + ja + la
        categorias = ca + al + ja + la

        # Tamanho do Vetor, incluindo o tamanho das refeições
        tam_combinacao = [len(ca), len(al), len(ja), len(la)]
        #tam_combinacao = [len(ca), len(al), len(ja)]


    # Customização do Objetivo NSGA-II - Desempenho:
        # Desempenho = -1*(Energia + Quantidade + Distribuição + Peso)
        # Energia
        #           [ [CM_min, CM_max], [A/J_min, A/J_max], [La_min, LA_max] ]
        #energia_refeicao = [[0.15, 0.35], [0.50, 0.80], [0.05, 0.15]]
        #       [ [CM_min, CM_max], [Al_min, Al_max], [Jan_min, Jan_max], [La_min, LA_max] ]
        energia_refeicao = [[0.15, 0.35], [0.15, 0.40], [0,15, 0.40],  [0.05, 0.15]]
        
        # Quantidade
        #           [ [CM_min, CM_max], [A/J_min, A/J_max], [La_min, LA_max] ]
        quantidade_refeicao = [[300, 500], [400, 500],[400, 500], [300, 500]]
        #          [ [CM_min, CM_max], [Al_min, Al_max], [Ja_minm JA_max], [La_min, La_max]]
        #quantidade_refeicao = [[300, 500], [400, 600],[400, 600]]
        
        # Peso
        #               [min, maximo ]
        peso_refeicao = [900, 2100] # Minimo e Máximo de Tolerável

        des = desempenho(tam_combinacao, energia_refeicao, quantidade_refeicao, peso_refeicao)
        fil = comida(['Pão, trigo, forma, integral','Laranja, lima, suco'],['cereais','bebidas'],[0,8]) #todas as listas devem ter o mesmo tamanho
    
        repetir_alimento = True # True = a combinação pode ter comida repetida
        repetir_alimento_ref = True #True = a refeição pode ter comida repetida
        juntar_almoço_jantar = False #True = almoço e jantar é 1, False = 1 e 2 serparados
        fixar_alimento = False
        
        if not repetir_alimento:
            repetir_alimento_ref = False
        
        ex = extras(repetir_alimento, repetir_alimento_ref, juntar_almoço_jantar,fixar_alimento)
    
        nutri = ['Proteina', 'Calcio','Sodio', 'FibraAlimentar', 'Ferro', 'VitaminaA']
        #nutri = ['Calcio', 'FibraAlimentar']
        dietary_intake = ['Proteina', 'Carboidrato','Colesterol']
        dietary_intake_percentage = [[0.45,0.65], [0.10,0.35], [0.20,0.35]]
        mn = macronutriente(dietary_intake,dietary_intake_percentage)

        nutricao = objetivos + nutri + dietary_intake
        restricao = nutri

        log = True

        print("\n+------------------------------------------------+")
        print("|          Problema da Dieta Alimentar           |")
        print("+------------------------------------------------+")
        print("| Feito por Vítor Pochmann (Otragal)             |")
        print("+------------------------------------------------+\n")
        print('\n CONFIGURAÇÃO PADRÃO:')
        print("1. Todos os valores dos nutrientes estão medidos por 100 gramas de alimento.")
        print("2. São 4 grupos de alimentos: Café da Manhã (CM), Almoço (Al), Jantar (Ja) e Lanche(La)")
        print("\nCOSTUMIZAÇÃO:")
        print("Deseja mudar a quantidade de gramas dos alimentos?\n Insere um valor de 1 à 10,")
        print(" 1 = 10 gramas; 2 = 20 gramas; 5 = 50 gramas; 7 = 70 gramas; 10 = 100 gramas (PADRÃO).")
        print(("\nSe tiver tudo certo, aperte ENTER para iniciar o programa..."))
        input("Press Enteraaaaaa to continue...")
        try:
            macro = Macro(usu, objetivos, qtd_objetivos, categorias, des, mn, fil, ex, nutricao, porcentagem, restricao)
            #macro = Macro(pessoa, idade, categorias, 
            #   tam_combinacao, energia_refeicao, quantidade_refeicao, peso_refeicao,
            #    nutricao, porcentagem, restricao)
            macro.inicizalizarGenes()
            macro.inicializarRestricao()
    
            condiMais = [('Energia1',2000, 'Energia1', 6000),('Preco',10, 'Preco',500)]
            

            alterncondi  = {'Calcio': 300}
    
            evoluir = GA(epocas,maxEpoca,maxPovo, macro, alter_condicoes=None, mais_condicoes=condiMais, log=log)
    
            evoluir.iniciar()
        
        finally:
            macro.quitProgram()

App()