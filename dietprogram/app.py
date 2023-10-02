import os
from macro import Macro
from ga import GA
import database
from filtros import comida, desempenho, usuario, extras, macronutriente

'''
Class App()

    Main python file to run the program

    __init__(self)
        It has some hyperparams of MUlti-Level Algorithm (NSGA-II & Gurobi):
            - epocas : epochs (int)
            - maxEpoca : range of epochs (int)
            - maxPovo : max length of population (int)
            - pessoas : type of person is (See Database files) (int)
            - idade : age (int)
            - porcentagem : porcentage of food distribution, with means X% for each food (int)

        The structure of App() is:

            OBJECTIVES: Two objetives:
                - String list []
                    - Energy (Energia1) 
                    - Price: (Preco)
            DAILY MENU: All meals that the user will eat in a day:
                - String list of categories []
                    - Breakfast (ca)
                    - Lunch (al)
                    - Dinner (ja)
                    - Snack (la)
                ( You can add or remove meals)
            UNITE VECTOR:
                - all the categories (categorias)
                - size of vector (tam_combinacao)
            CONCENTRATION SETTINGS
                You can costumizate one of NSGA-II Objective - Concentration.
                But here, we refer the Concentration as "Desempenho" variable.

                The function of Concentration or Desempenho is:
                    Desempenho = -1*(Energia + Quantidade + Distribuição + Peso)
                        - Energia: Energy of food in Candidate Solution
                        - Quantidade: Amount of food in Candidate Solution
                        - Distribuição: Distribution of food in Candidate Solution*
                        - Peso: Weigth of food in Candidate Solution
                    *Only "Distribuição" is uneditable!
        
                The other three params of "Desempenho" function can edit and they have min and max values that refers to the nutrient consumption tolerance interval.
                That is, they are a part of the constraints of Gurobi.
                To edit theses params, follow the example energy constraint:

                                            Breakfast           Lunch           Dinner       Others
                                       [ [ min,    max   ], [ min,   max  ], [ min,  max  ], [...] ]
                    energia_refeicao = [ [ 0.15,   0.35  ], [ 0.15,  0.80 ], [ 0.05, 0.15 ], [...] ]
                
                If you defined 4 meals, the "energia_refeicao" and "quantidade_refeicao" must have 4 [min, max] values in the list.
                As same as you define 3 meals, they must have 3 [min, max ] values 

                But the "peso_refeicao" has one [min, max] values.

    Also it has two kind of examples cases to execute this program.
    To switch examples, just copy & paste the settings below:
'''
# Example 1
'''
        # Define categories for each meal
        ca = ['cereais', 'leites', 'frutas'] # Breakfast
        al = ['cereais', 'leguminosas', 'verduras', 'carnes', 'ovos'] # Lunch
        ja = ['bebidas', 'verduras', 'pescados', 'leites'] # Dinner
        la = ['verduras', 'gorduras', 'frutas'] # Snack

        # Unite Vector
        categorias = ca + al + ja + la
        tam_combinacao = [len(ca), len(al), len(ja), len(la)]

        # Constraints of Concentration/Desempenho
        # Energy
        energia_refeicao = [[0.15, 0.35], [0.15, 0.40], [0,15, 0.40],  [0.05, 0.15]]
        
        # Amount
        quantidade_refeicao = [[300, 500], [400, 500],[400, 500], [300, 500]]

        # Weight
        peso_refeicao = [900, 2100] # Minimum and Maximum Tolerable
'''
# Exemple 2
'''
        # Define categories for each meal
        ca = ['cereais', 'carnes', 'carnes', 'leguminosas', 'leguminosas', 'verduras'] # Breakfast
        al = ['cereais','carnes','ovos', 'leguminosas','verduras','verduras'] # Lunch
        ja = ['cereais', 'pescados','ovos', 'verduras', 'verduras'] # Dinner

        # Unite Vector
        categorias = ca + al + ja + la
        tam_combinacao = [len(ca), len(al), len(ja)]

        # Constraints of Concentration/Desempenho
        # Energy
        energia_refeicao = [[0.15, 0.35], [0.50, 0.80], [0.05, 0.15]]
        
        # Amount
        quantidade_refeicao = [[300, 500], [400, 600],[400, 600]]

        # Weight
        peso_refeicao = [900, 2200] # Minimum and Maximum Tolerable
'''

class App():
    
    
    def __init__(self):
        print("Iniciando...\n")

        epocas = 0
        maxEpoca = 8 # Default 8
        maxPovo = 100 # Default: 100

        pessoa = 3 # Default: 3 (man adult)
        idade = 25 # Default: 25 (years old)
        porcentagem = 10 # Default: 10 (10% of distribution)

        usu = usuario(pessoa, idade, porcentagem)
    
    '''
    OBJECTIVES
    '''

        qtd_objetivos = 2 # Default: 2 (two use more, needs add one in "objetivos")
        objetivos = ['Energia1', 'Preco'] # Default: objetivos = ['Energia1', 'Preco']

    '''
        PASTE EXAMPLE HERE ###################################################################
    '''
        # Define categories for each meal
        ca = ['cereais', 'leites', 'frutas'] # Breakfast
        al = ['cereais', 'leguminosas', 'verduras', 'carnes', 'ovos'] # Lunch
        ja = ['bebidas', 'verduras', 'pescados', 'leites'] # Dinner
        la = ['verduras', 'gorduras', 'frutas'] # Snack

        # Unite Vector
        categorias = ca + al + ja + la
        tam_combinacao = [len(ca), len(al), len(ja), len(la)]

        # Constraints of Concentration/Desempenho
        # Energy
        energia_refeicao = [[0.15, 0.35], [0.15, 0.40], [0,15, 0.40],  [0.05, 0.15]]
        
        # Amount
        quantidade_refeicao = [[300, 500], [400, 500],[400, 500], [300, 500]]

        # Weight
        peso_refeicao = [900, 2100] # Minimum and Maximum Tolerable
    
    '''
        EXAMPLE ENDS HERE ##################################################################
    '''

        # Instantiates the Desempenho
        des = desempenho(tam_combinacao, energia_refeicao, quantidade_refeicao, peso_refeicao)

    '''
    FILTERS
    
        Its new feature but still developtment.

        There are few filters work in this system:
        
        1) Fix Food Filter:
            - Use comida() class to define this filter and a boolean variable to turn on or off.
            - In the diet scope, you want a food to always be present in one or more meals and not be replaced by other foods during computation. 
            - So you need add this food and where it will be added.
            - You need to know the name and index of vector "Unite Vector".
            - True: turn on this filter.
            - False: turn off this filter.

            Example: 
                White bread in the breakfast as the first food and orange juice in the dinner as the first food;
                fil = comida(['Pão, trigo, forma, integral','Laranja, lima, suco'],['cereais','bebidas'],[0,8])
        2) Repeat Food Filter:
            - Boolean variable that define if the combination can repeat food to fill the categories
            - True: the combination CAN repeat food
            - False: the combination CANNOT repeat food
        3) Repeat Food Meal Filter:
            - Boolean variable that define if the meal can repeat food to fill the categories
            - Meals cannot repeat foods, but the same food can be repeated for each meal.
            - True: CAN repeat
            - False: CANNOT repeat

        FILTER NOT IMPLEMENTED:

        1) Merge Lunch and Dinner Filter:
            - Sometimes people eat the same food for dinner as they had for lunch.
            - To facilitate the computation of meals, there is a filter that mixes lunch and dinner foods and automatically arranges the other important variables of the scope of the diet.
            - This filter is not implemented.
    '''

        # Fix Food Filter - Comida()
        fix_food = comida(['Pão, trigo, forma, integral','Laranja, lima, suco'],['cereais','bebidas'],[0,8]) #todas as listas devem ter o mesmo tamanho
        fixar_alimento = False

        # Others filters
        repetir_alimento = True # True = a combinação pode ter comida repetida
        repetir_alimento_ref = True #True = a refeição pode ter comida repetida
        juntar_almoço_jantar = False #True = almoço e jantar é 1, False = 1 e 2 serparados
        
        
        if not repetir_alimento:
            repetir_alimento_ref = False
        
        # Instantiates the Filters as ex
        ex = extras(repetir_alimento, repetir_alimento_ref, juntar_almoço_jantar,fixar_alimento)
    '''
    CONSTRAINTS

        Here, add nutrients restrictions that are presented in database.
        You can put as much nutrients as you want, but you can't repeat.

        Each nutrient has a minimum and maximum value that vary and respect the gender and age of the user.
    '''
        nutri = ['Calcio','Sodio', 'FibraAlimentar', 'Ferro', 'VitaminaA']
        
    '''
    DIETARY INTAKE

        Not all nutrients are measured by weight.
        Macronutrients depend on the total amount of energy in the food composition.
        Protein, Carbohydrate and Cholesterol are the macronutrients.
        Your healthy ranges are the percentages of the total energy of the composition and your default values are:
            - Proteina: [0.45, 0.65]
            - Carboidrato: [0.10, 0.35]
            - Colesterol: [0.20, 0.35]

        On the other hand, it is possible to change them.
    '''
        # Names of macronutrients
        dietary_intake = ['Proteina', 'Carboidrato','Colesterol']
        # Interval of them
        dietary_intake_percentage = [[0.45,0.65], [0.10,0.35], [0.20,0.35]]
        # Instantiates them
        mn = macronutriente(dietary_intake,dietary_intake_percentage)

        # Concatenate
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
        input("Press Enter to continue...")
        try:
            macro = Macro(usu, objetivos, qtd_objetivos, categorias, des, mn, fix_food, ex, nutricao, porcentagem, restricao)
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