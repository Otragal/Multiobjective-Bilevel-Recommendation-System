import os
from macro import Macro
from ga import GA
import database
from filtros import comida, desempenho, usuario, extras

class App():
    
    
    def __init__(self):
        print("Iniciando...\n")

        epocas = 0
        maxEpoca = 8
        maxPovo = 100

        pessoa = 3
        idade = 25
        porcentagem = 10

        usu = usuario(pessoa, idade, porcentagem)

        #Objetivos
        objetivos = ['Energia1', 'Preco']
    
    # Cardápio Diário:
        # Café da Manhã
        ca = ['cereais', 'leites', 'frutas']
        # Almoço
        al = ['cereais','leguminosas','verduras', 'carnes','ovos']
        # Jantar
        ja = ['bebidas', 'leguminosas','pescados', 'nozes']
        # Lanche
        la = ['verduras', 'gorduras', 'frutas']

        # Criação do Vetor Unitário:
        # Vetor
        categorias = ca + al + ja + la
        # Tamanho do Vetor, incluindo o tamanho das refeições
        tam_combinacao = [len(ca), len(al), len(ja), len(la)]

    # Customização do Objetivo NSGA-II - Desempenho:
        # Desempenho = -1*(Energia + Quantidade + Distribuição + Peso)
        # Energia
        #           [ [CM_min, CM_max], [A/J_min, A/J_max], [La_min, LA_max] ]
        #energia_refeicao = [[0.15, 0.35], [0.50, 0.80], [0.05, 0.15]]
        #       [ [CM_min, CM_max], [A/J_min, A/J_max], [La_min, LA_max] ]
        energia_refeicao = [[0.15, 0.35], [0.15, 0.40], [0,15, 0.40], [0.05, 0.15]]
        
        # Quantidade
        #           [ [CM_min, CM_max], [A/J_min, A/J_max], [La_min, LA_max] ]
        #quantidade_refeicao = [[30, 50], [40, 50],[40, 50], [30, 50]]
        #          [ [CM_min, CM_max], [Al_min, Al_max], [Ja_minm JA_max], [La_min, La_max]]
        quantidade_refeicao = [[30, 50], [40, 60],[40, 60], [30, 50]]
        
        # Peso
        #               [min, maximo ]
        peso_refeicao = [900, 2100] # Minimo e Máximo de Tolerável
    
        des = desempenho(tam_combinacao, energia_refeicao, quantidade_refeicao, peso_refeicao)
        fil = comida(['Pão, trigo, forma, integral','Laranja, lima, suco'],['cereais','bebidas'],[0,8]) #todas as listas devem ter o mesmo tamanho
    
        repetir_alimento = True # Ture = a combinação não pode ter a mesma comida
        juntar_almoço_jantar = False #True = almoço e jantar é 1, False = 1 e 2 serparados
        fixar_alimentos = True
    
        ex = extras(repetir_alimento,juntar_almoço_jantar,fixar_alimentos)
    
        nutri = ['Proteina', 'Carboidrato','Calcio', 'Sodio','FibraAlimentar', 'Ferro', 'VitaminaA']
        
        nutricao = objetivos + nutri
        restricao = nutri
    
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
        input("Press Enter to continue...")
        try:
            macro = Macro(usu, categorias, des, fil, ex, nutricao, porcentagem, restricao)
            #macro = Macro(pessoa, idade, categorias, 
            #   tam_combinacao, energia_refeicao, quantidade_refeicao, peso_refeicao,
            #    nutricao, porcentagem, restricao)
            macro.inicizalizarGenes()
            macro.inicializarRestricao()
    
    
    
            condiMais = [('Energia1',2000, 'Energia1', 6000),('Preco',10, 'Preco',500)]
            alterncondi  = {'Calcio': 300}
    
            evoluir = GA(epocas,maxEpoca,maxPovo, macro, alter_condicoes=None, mais_condicoes=condiMais, log=True)
    
            evoluir.iniciar()
        
        finally:
            macro.quitProgram()
    