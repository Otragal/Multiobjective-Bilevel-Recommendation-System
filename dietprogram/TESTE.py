# Demonstração resumida de todo o programa:

import os
from fitnessGurobi import FitnessGurobi
from macro import Macro
from individuo import Individuo
from formatConverter import FormatConverter
from gurobyModel import GurobiModel
from genetic import Genetic

# 1) Define as informações do Usuário
pessoa = 3
idade = 25
porcentagem = 0.1
categorias = ['cereais','leites','frutas','cereais','verduras','leguminosas','carnes','cereais','leites','frutas']

#nutricao = ['Energia1','Proteina', 'Calcio', 'FibraAlimentar']
#nutRestricao = ['Proteina', 'Calcio', 'FibraAlimentar']
objectivos = ['Energia1','Preco']
nutricao1 = ['Proteina','FibraAlimentar','Calcio','Cobre','Ferro','Sodio','Magnesio','Fosforo','Zinco','VitaminaA','VitaminaC']
nutricao = objectivos + nutricao1
print(nutricao)

nutRestricao = nutricao1
print(nutRestricao)

# 2) Cria um Macro para armazenar informações e gerar os genes e restrições
#   O Macro serve como Pacote que armazena informações de alimentos desejados pelo Usuário
macro = Macro(pessoa, idade, categorias, nutricao, porcentagem, nutRestricao)
macro.inicizalizarGenes(categorias)
macro.inicializarRestricao()

# 3) Instanciliza o Genetic Algorithm (GA) para preparar a busca da melhor respsta
#   Dentro de N alimentos das Categorias escolhidas pelo Usuário

# 4) Dentro do GA, inicializa a 1ª população
#   Nesta população contém X inidíviduos
#   Para cada indivíduo, contém uma conjunto de um alimento para cada categoria

pessoa1 = Individuo(macro.getGenes())
pessoa2 = Individuo(macro.getGenes())
print("PESSOA:")
pessoa1.printIndividuo()
print("Cromossomo: ", pessoa1.size())
pessoa1.printIndividuoAll()
# 5) Inicia o loop de gerações (epocas)
#   Para cada época, realiza torneio para selecionar os indivíduos escolhidos a se procriarem
#   Para cada torneio, escolhe X pessoas, o vencedor é aquele que tiver o melhor fitness

novaPessoa = Genetic.crossover(pessoa1, pessoa1, log=True)
novaPessoa = Genetic.mutation(novaPessoa, macro,log=True)

# 5.1) Realiza as variáveis desejadas para computar o model Gurobi

# Converte para pegar valores, nomes, energia
val,name,energy,price = FormatConverter.getValuesNamesEnergy(novaPessoa.cromossomo, porcentagem)

print("\nVAL: ","LEN: ",len(val))

for i in range(len(val)):
    print(val[i],'; ', end='')
    if i%6 == 0:
        print(';\n')
    

print("\nNAME:", "LEN: ",len(name))
print(name)
print("\nENERGY:","LEN: ",len(energy))
print(energy)
print("\nPRICE:","LEN: ",len(price))
print(price)
varNuts = FormatConverter.makeDictNutriValues(name,macro.nutricao,val,porcentagem) #Convert para formar os varNuts
print("\nVARNUTS:")
print(varNuts)

minCons = FormatConverter.makeDictNutrition(macro.nutRestricao,macro.restricaoMIN)
maxCons = FormatConverter.makeDictNutrition(macro.nutRestricao, macro.restricaoMAX)

FormatConverter.addOneDictNutrition('Energia1',2000,minCons)
FormatConverter.addOneDictNutrition('Energia1',3400,maxCons)
FormatConverter.addOneDictNutrition('Preco',10,minCons)
FormatConverter.addOneDictNutrition('Preco',500,maxCons)
print("\nMINCONS:")
print(minCons)
print("\nMAXCONS:")
print(maxCons)
# 5.2) Realiza o Solve do Model Gurobi
model = GurobiModel.createModel("teste1")
model2 = GurobiModel.createModel("teste2")
print("")
print("Macro.nutricao|Constrains")
print(macro.nutricao)
print("\nName|Variables")
print(name)
print("\nEnergy|Objective")
print(energy)
print("\nVarNuts|ValuesConstrains")
print(varNuts)
print("\nMaxCons|maxConstrains")
print(maxCons)
print("\nMinCons|minConstrains")
print(minCons)
model, resultado = GurobiModel.solveModel(model,macro.nutRestricao, name, energy, varNuts, maxCons,minCons)
# FAZER O SEGUNDO MODEL ONDE PROTEINA, CARBOIDRATO E VET DEPENDEM DO RESULTADO DO MODEL1
GurobiModel.printSolution(model)

print(resultado)
print(energy)
print(price)
novaPessoa.setFitness(FitnessGurobi.fitness(resultado,energy,price, porcentagem))

# 5.3) Com a respota do Solve, computa o Fitness baseado a resposta do Solver

# 6) Realiza a criação do novo indivíduo e ele é armazenado na nova população

# 7) Uma vez atingido uma número desejado para a nova população, volta para o 5)
#   O loop de épocas só vai parar quando atingir certo número de épocas

# 8) Printa a melhor indivíduo
