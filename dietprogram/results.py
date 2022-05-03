import matplotlib.pyplot as plt
from collections import defaultdict

import numpy as np
import pandas as pd
import math
import csv

mg = ['Calcio', 'Magnesio','Potassio', 'Zinco', 'Riboflavina',
    'Ferro', 'Sodio','Colesterol', 'Manganes', 'Fosforo',
    'Cobre', 'VitaminaC', 'Tiamina', 'Niacina']

mcg = ['VitaminaA']

class Results:

    def createFrontsCSV(self, povo, macro):
        header = []
        header.extend(["Indivíduo"])
        for cat in macro.categoria:
            header.extend([cat])
        header.extend(["Concentração"])
        header.extend(["Custo"])
        header.extend(["Energia Total"])
        print(header)
        with open('resultados.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            # Write Soluções Dominadas
            for key,i in enumerate(povo.individuos):
                individuo = []
                individuo.append(key)
                for gene in i.cromossomo:
                    individuo.append(gene[0])
                
                individuo.extend(i.fitness)
                #print(i.atributos[1])
                #print(sum(i.atributos[1]))
                sumEner = np.dot(i.atributos[0],i.atributos[1])
                individuo.append(sumEner)
                writer.writerow(individuo)
            # Write Soluções Não Dominadas
            for key,i in enumerate(povo.fronts[0]):
                individuo = []
                individuo.append(key)
                for gene in i.cromossomo:
                    individuo.append(gene)
                individuo.extend(i.fitness)
                sumEner = np.dot(i.atributos[0],i.atributos[1])
                individuo.append(sumEner)
                writer.writerow(individuo)
        
        print('Finished 1')
            

    def saveFronts(self, povo, macro, epoca):
            
            if macro.porcentagem is not None and macro.porcentagem != 0:
                percent = ', alimento com {}g'.format(macro.porcentagem)
            desempenho  = []
            dfront = []
            custo = []
            cfront = []
            for i in povo.individuos:
                fitness = i.getFitness()
                desempenho.append(fitness[0])
                custo.append(fitness[1])
            for i in povo.fronts[0]:
                fitness = i.getFitness()
                dfront.append(fitness[0])
                cfront.append(fitness[1])
            plt.plot(desempenho, custo, 'bo', dfront, cfront, 'ro')
            #plt.title("NSGA-II with Gurobi - Diet Problem - Pareto-Optimal"+percent)
            #plt.xlabel('Concentration (Smaller is Better)')
            #plt.ylabel(('Cost per Unit (Lower is Better)'))
            plt.title("NSGA-II com Gurobi - Problema da Dieta - Pareto-Optimal"+percent)
            plt.xlabel('Concentração (Menor é Melhor)')
            plt.ylabel(('Custo Unitário (Menor é Melhor)'))
            if epoca >= 0:
                plt.savefig('/home/otragal/Workspace/Multiobjective-Bilevel-Recommendation-System/dietprogram/pics/teste10Epoca{}.png'.format(epoca))
            else:
                print('Error Epoca < 0')
            plt.close()

    def plotFronts(self, povo, macro):
        
        if macro.porcentagem is not None and macro.porcentagem != 0:
            percent = ', alimento com {}g'.format(macro.porcentagem)
        desempenho  = []
        dfront = []
        custo = []
        cfront = []
        for i in povo.individuos:
            fitness = i.getFitness()
            desempenho.append(fitness[0])
            custo.append(fitness[1])
        for i in povo.fronts[0]:
            fitness = i.getFitness()
            dfront.append(fitness[0])
            cfront.append(fitness[1])
        plt.plot(desempenho, custo, 'bo', dfront, cfront, 'ro')
        plt.title("NSGA-II com Gurobi - Problema da Dieta - Pareto-Optimal"+percent)
        plt.xlabel('Concentração (Menor é Melhor)')
        plt.ylabel(('Custo Unitário (Menor é Melhor)'))
        plt.show()

    def plotFrontsIntakes(self, povo, macro):
        if macro.porcentagem is not None and macro.porcentagem != 0:
            percent = 'Non-Dominatted Candidate Solutions Nutritions, food with '.format(macro.porcentagem)
        else:
            percent = 'Non-Dominatted Candidate Solutions Nutritions'
        width = 0.35
        legenda = "Solution "
        index_intake = 4

        plot_each_food_intakes = []

        for ind in povo.fronts[0]:
            gene_intake = []
            for index, gene in enumerate(ind.cromossomo):
                intakes = []
                #print('Comida: '+ gene[0])
                for nutri in range(index_intake,len(gene)-macro.macronutriente.tamanho):
                    
                    #print('Intake: %.2f' % gene[nutri])
                    #print('Qtd = %.2f ' % ind.atributos[0][index])
                    intakes.append(gene[nutri]*ind.atributos[0][index])
                    
                gene_intake.append(intakes)
            sum_intakes = [sum(i) for i in zip(*gene_intake)]
            if macro.porcentagem is not None and macro.porcentagem != 0:
                sum_intakes = [i/macro.porcentagem for i in sum_intakes]
            for i in range(len(macro.nutRestricao)):
                if macro.nutRestricao[i] in mg:
                    sum_intakes[i] = sum_intakes[i]/1000
                if macro.nutRestricao[i] in mcg:
                    sum_intakes[i] = sum_intakes[i]/1000000
            plot_each_food_intakes.append(sum_intakes)
        
        print(plot_each_food_intakes)
        #numpy_array = np.array(plot_each_food_intakes)
        #transpose = numpy_array.T
        #transpose_list = transpose.tolist()

        df = pd.DataFrame(plot_each_food_intakes,columns=macro.nutRestricao)

        print(df)
        df.plot(kind='bar', stacked=True, title=percent)
        plt.grid(axis='y', linestyle='--')
        plt.legend(loc="upper left", ncol=math.ceil(len(macro.nutRestricao)/2))
        plt.xlabel('Candidate Solutions')
        plt.ylabel('Amount of Food Nutrition (g)')
        plt.show()
        
    def plotFrontFoods(self, povo, macro):
        if macro.porcentagem is not None and macro.porcentagem != 0:
            percent = 'Distribution of Food Category for each Non-Dominated Candidate Solutions, food with'.format(macro.porcentagem)
        else:
            percent = 'Distribution of Food Category for each Non-Dominated Candidate Solutions'
        

        legenda = "Solution "
        plot_each_food = []

        duplicada, duplas = Results().find_duplication(macro.categoria)
        list_index_cat = [i for i in range(len(macro.categoria))]
        list_index_cat = set(list_index_cat)
        duplicada = set(duplicada)
        mono_food = list(list_index_cat - duplicada)

        lista_cat = []
        
        # legenda
        for dupla in duplas:
            lista_cat.append(macro.categoria[dupla[0]])
        for mono in mono_food:
            lista_cat.append(macro.categoria[mono])
        
        for ind in povo.fronts[0]:
            gene_food = []
        
            # making legenda
            for dupla in duplas:
                count = 0
                for i in range(len(dupla)):
                    count = count +ind.atributos[0][i]
                gene_food.append(count)

            for mono in mono_food:
                gene_food.append(ind.atributos[0][mono])

            plot_each_food.append(gene_food)
                    
         
        print(plot_each_food)
        #numpy_array = np.array(plot_each_food)
        #transpose = numpy_array.T
        #transpose_list = transpose.tolist()

        df = pd.DataFrame(plot_each_food,columns=lista_cat)

        print(df)
        df.plot(kind='bar', stacked=True, colormap='tab10', title=percent)
        plt.grid(axis='y', linestyle='--')
        plt.legend(loc="upper left", ncol=math.ceil(len(lista_cat)/2))
        plt.xlabel('Candidate Solutions')
        plt.ylabel('Quantity of Food Category')
        plt.show()


    def boxSplotMacronutrientes(self, povo, macro):
        if macro.porcentagem is not None and macro.porcentagem != 0:
            percent = 'Distribution of Macronutrients in Non-Dominated Candidate Solutions, food with {}g'.format(macro.porcentagem)
        else:
            percent = 'Distribution of Macronutrients in Non-Dominated Candidate Solutions'
        width = 0.35
        legenda = "Solution "

        box_macro = []

        for ind in povo.fronts[0]:
            gene_intake = []
            for index, gene in enumerate(ind.cromossomo):
                intakes = []
                #print('Comida: '+ gene[0])
                for nutri in gene[-macro.macronutriente.tamanho:]:
                    #print('Intake: %.2f' % nutri)
                    #print('Qtd = %.2f ' % ind.atributos[0][index])
                    intakes.append(nutri*ind.atributos[0][index])
                
                gene_intake.append(intakes)
            
            sum_macro = []
            for i in range(macro.macronutriente.tamanho):
                unit_macro = []
                for j in gene_intake:
                    if macro.porcentagem is not None and macro.porcentagem != 0:
                        unit_macro.append(j[i]/macro.porcentagem)
                    else:
                        unit_macro.append(j[i])

                sum_macro.append(unit_macro)
            
            box_macro.append(sum_macro)
        
        print(box_macro)
        tamanho_individuos = len(box_macro)
        
        
        if (tamanho_individuos % 2) == 0:
            if tamanho_individuos > 2:
                div_plt = int(tamanho_individuos/2)
        else:
            
            tamanho_individuos += 1
            div_plt = int(tamanho_individuos/2)
            even = False
        fig, axs = plt.subplots(2, div_plt)
        
        for i in range(div_plt):
            axs[0,i].boxplot(box_macro[i], labels=macro.macronutriente.nomes_macro)
            axs[0,i].set_title('{} {}'.format(legenda, i))
        
        
        for index,i in enumerate(range(div_plt,len(box_macro))):
            axs[1,index].boxplot(box_macro[i], labels=macro.macronutriente.nomes_macro)
            axs[1,index].set_title('{} {}'.format(legenda, i))
        
        plt.show()
        
    def stackBarEnergyMacro(self, povo, macro):
        if macro.porcentagem is not None and macro.porcentagem != 0:
            percent = 'Percentage of Macronutrients in Non-Dominated Candidate Solutions, food with {}g'.format(macro.porcentagem)
        else:
            percent = 'Percentage of Macronutrients in Non-Dominated Candidate Solutions'
        

        legenda = "Solução "

        box_macro = []
        box_energy = []
        for ind in povo.fronts[0]:
            VET = float(np.dot(ind.atributos[0],ind.atributos[1]))
            gene_intake = []
            for index, gene in enumerate(ind.cromossomo):
                intakes = []
                #print('Comida: '+ gene[0])
                for nutri in gene[-macro.macronutriente.tamanho:]:
                    #print('Intake: %.2f' % nutri)
                    #print('Qtd = %.2f ' % ind.atributos[0][index])
                    intakes.append(nutri*ind.atributos[0][index])
                
                gene_intake.append(intakes)
            sum_intakes = [sum(i) for i in zip(*gene_intake)]
            
            if macro.porcentagem is not None and macro.porcentagem != 0:
                sum_intakes = [i/macro.porcentagem for i in sum_intakes]
            #for i in range(len(macro.macronutriente.nomes_macro)):
            #    if macro.macronutriente.nomes_macro[i] in mg:
            #        sum_intakes[i] = sum_intakes[i]/1000
            #    if macro.macronutriente.nomes_macro[i] in mcg:
            #        sum_intakes[i] = sum_intakes[i]/1000000
            sum_intakes_percentage = sum_intakes.copy()
            sum_intakes_percentage = [(i/VET)*100 for i in sum_intakes_percentage]
            box_macro.append(sum_intakes_percentage)
            
            box_energy.append(VET)
        
        print(box_macro)
        tamanho_individuos = len(box_macro)
        if (tamanho_individuos % 2) == 0:
            div_plt = int(tamanho_individuos/2)
        else:
            tamanho_individuos += 1
            div_plt = int(tamanho_individuos/2)
            even = False
        fig, axs = plt.subplots(2, div_plt)

        for i in range(div_plt):
            axs[0,i].pie(box_macro[i], labels=macro.macronutriente.nomes_macro, autopct='%1.1f%%', shadow=True, startangle=90)
            axs[0,i].axis('equal')
            axs[0,i].set_title('{} {}'.format(legenda, i))
        
        for index,i in enumerate(range(div_plt,len(box_macro))):
            axs[1,index].pie(box_macro[i], labels=macro.macronutriente.nomes_macro, autopct='%1.1f%%', shadow=True, startangle=90)
            axs[1,index].axis('equal')
            axs[1,index].set_title('{} {}'.format(legenda, i))

        plt.show()


    @staticmethod
    def find_duplication(codigo, log=None):
        duplicada = []
        d = defaultdict(list)
        for i,item in enumerate(codigo):
            d[item].append(i)

        for k,v in d.items():
            if len(v)>1:
                duplicada.extend(v)

        dupla = [v for k,v in d.items() if len(v)>1]
        if log:
            print('Genetic::find_duplication\t Existe duplicação')
            print(duplicada)
        return duplicada, dupla