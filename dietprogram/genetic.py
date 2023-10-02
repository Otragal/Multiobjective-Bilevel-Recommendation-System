from fitnessGurobi import FitnessGurobi
from gurobyModel import GurobiModel
from formatConverter import FormatConverter
from individuo import Individuo
from collections import defaultdict
from povo import Povo


import math
import pandas as pd
import numpy as np
import random
import csv 


"""
Class Genetic()

    Contains NSGA-II functions and methods

    evoluir_NSGA()
        NSGA-II algorithm;

    combine_first_population()
        Method to perform the first combination of the current population with the children;

    crossover()
        Uniform crossover method 50%;

    mutation()
        Uniform mutation method 50% for each gene;

    torneio()
        Selection method Tournament of 2 or 5 individuals;

    crowding_operator()
        NSGA-II Crowding Operator Method, selection operator;

    fast_nondominated_sort()
        NSGA-II fast-nondominated-sort method;    

    calculate_crowding_distance()
        NSGA-II crowding-distance calculation method;

    make_new_pop()
        Method for creating a new NSGA-II population;

 Example Candidate Solution with a Scope Diet
 Categoria : ['cereais','leites','frutas','verduras','leguminosas','carnes','pescados']
 Indice:     [     1,      2,      3,         4,           5,         6,       7]

"""

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
            print('Genetic::find_duplication\t There is duplication')
            print(duplicada)
        return duplicada, dupla


class Genetic():

    crossoverUniforme = 0.5
    mutationValue = 0.4
    tamanhoTorneio = 5
    chanceTorneio = 0.9

    @staticmethod
    def evoluir_NSGA(povo, macro, maxPovo, model, model_name, log=None):
        
        # Geration of Q(t)
        povo = Genetic.combine_first_population(povo, macro, model,model_name)
        # F = fast-non-dominated-sort(Rt)
        povo = Genetic.fast_nondominated_sort(povo)
        # P(t+1) = None
        novoPovo = Povo()
        # i = 0
        front_number = 0
        # until |P(t+1)| + |F(i)| <= N
        while (novoPovo.size() + len(povo.fronts[front_number])) <= maxPovo:
            # crowding-distance-assigment(Fi)
            povo.fronts[front_number] = Genetic.calculate_crowding_distance(povo.fronts[front_number])
            # P(t+1) = P(t+1) U F(i)
            novoPovo.extend(povo.fronts[front_number])
            # i = i + 1
            front_number += 1

        # Need to do crwonding_distance on F(i) before Sort(F(i), <n)        
        povo.fronts[front_number] = Genetic.calculate_crowding_distance(povo.fronts[front_number])        
        # Sort(Fi, <n)
        povo.fronts[front_number].sort(key=lambda individuo: individuo.crowding_distance, reverse=True)
        # P(t+1) = P(t+1) U f(i)[ 1 : (N - |P(t+1)| )]
        novoPovo.extend(povo.fronts[front_number][0:(maxPovo-novoPovo.size())])
        
        return novoPovo, povo

    @staticmethod
    def combine_first_population(povo, macro, model, model_name):
        povo = Genetic.fast_nondominated_sort(povo)
        for front in povo.fronts:
            front = Genetic.calculate_crowding_distance(front)
        Qt = Genetic.make_new_pop(povo, macro, model, model_name)
        povo.extend(Qt)
        return povo


    @staticmethod
    def crossover(ind1, ind2, macro,log=None):
        filho = Individuo()

        for i in range(ind1.size()):    
            if random.random() < Genetic.crossoverUniforme:
                filho.applyGene(ind1.getGene(i))
            else:
                filho.applyGene(ind2.getGene(i))
        
        if log:
            print("Genetic::crossover\t Realizando Crossover:")
            print(' Ind 1: ', end='')
            ind1.printIndividuo()
            print(' Ind 2: ', end='')
            ind2.printIndividuo()
            print('Crossover: !')
            filho.printIndividuo()
        return filho
    
    @staticmethod
    def mutation(individuo, macro, log=None):
        
        duplicada, dupla = find_duplication(individuo.codigo, log)
        duplicada_ref = []
        
        # repeat_food filter
        if not macro.extra.repetir_alimento and len(duplicada)>0:
            # fix_food filter
            if macro.extra.fixar_alimento:
                for i in duplicada:
                    if i in macro.filtro.indice:
                        duplicada.pop(i)
            
        else:
            # filter repeat food only at meals
            if not macro.extra.repetir_alimento_ref and len(dupla)>0:
                if len(dupla[0]>0):
                    # filter fix food
                    if macro.extras.fixar_alimento:
                        for dp in dupla:
                            for i in range(len(dp)):
                                if dp[i] in macro.filtro.indice:
                                    dp.pop(i)
            
                    point = 0
                    for ref in macro.desempenho.tam_categoria:
                        for dp in dupla:
                            a = set(dp) # Ex -> 1:{1,2,7}, 2:{3,5,6,8}
                            b = set(range(point,(point+ref))) # -> 1:{1,2,3}, 2:{4,5,6,7}
                            c = list(a & b) # -> 1:{1,2}, 2:{5,6}
                            if len(c) > 1:
                                duplicada_ref.extend(list(c)) # -> 1:[1,2], 2:[1,2,5,6]
        
        for i in range(individuo.size()):
            if not macro.extra.repetir_alimento and i in duplicada:
                individuo.setGene(i, macro.taco.selectRandomRestrictFood(macro.categoria[i], individuo.codigo[i], macro.nutricao))
            else:
                if not macro.extra.repetir_alimento and i in duplicada_ref:
                    individuo.setGene(i, macro.taco.selectRandomRestrictFood(macro.categoria[i], individuo.codigo[i], macro.nutricao))
                else:
                    if random.random() < Genetic.mutationValue:
                        individuo.setGene(i, macro.taco.selectRandomFood(macro.categoria[i], macro.nutricao))
                    

        if log:
            print("Genetic::mutation\t Individuo Mutato:")
            individuo.printIndividuo()
        
        return individuo
    
    
    @staticmethod
    def torneio(povo, log=None):
        torneio = random.sample(povo.individuos, Genetic.tamanhoTorneio)

        if (log):
            print("Genetic::torneio\t Competidores:")
            index = 0
            for i in torneio:
                print('[',index+1,'] ', end='')
                i.printIndividuo()
                index +=1
        
        melhor_participante = torneio[1]

        for participante in torneio:
            if (Genetic.crowding_operator(participante, melhor_participante) and (random.random() <= Genetic.chanceTorneio)):
                melhor_participante = participante

        if (log):
            print("Genetic::torneio\t Finalizado:\n", end='')
            melhor_participante.printIndividuo()
        return melhor_participante


    # NSGA-II - crowding operator
    @staticmethod
    def crowding_operator(individuo, outro_individuo):
        if (individuo.rank < outro_individuo.rank) or \
            ((individuo.rank == outro_individuo.rank) and (individuo.crowding_distance > outro_individuo.crowding_distance)):
            return True
        else:
            return False

    # NSGA-II - fast nondominated sort
    @staticmethod
    def fast_nondominated_sort(population):
        # Starts the Pareto frontier
        population.fronts = [[]]
        # for each p ( P 
        for individuo in population.individuos:
            # Domination count, np = 0 (number of solutions which dominate the solution p)
            individuo.domination_count = 0
            # Set of solutions that the solution p dominates, Sp = None
            individuo.dominated_solutions = []
            # for each q ( P
            for outro_individuo in population.individuos:
                # if p dominates q then
                if individuo.dominates(outro_individuo):
                    # Sp = Sp U {q}
                    individuo.dominated_solutions.append(outro_individuo)
                # else if q dominates p then
                elif outro_individuo.dominates(individuo):
                    # np = np + 1
                    individuo.domination_count += 1
            # if np = 0 then
            if individuo.domination_count == 0:
                # prank = 1 (primeiro indice)
                individuo.rank = 0
                # F1 = F1 U {p}
                population.fronts[0].append(individuo)
        # i = 1 (first index)
        i = 0
        # while Fi != None
        while len(population.fronts[i]) > 0:
            Qfront = [] # Q = None
            # for each p ( Fi
            for individuo in population.fronts[i]:
                # for each q ( Sp
                for outro_individuo in individuo.dominated_solutions:
                    # nq = nq - 1
                    outro_individuo.domination_count -= 1
                    # if nq = 0 then
                    if outro_individuo.domination_count == 0:
                        # qrank = i+1
                        outro_individuo.rank = i+1
                        # Q = Q U {q}
                        Qfront.append(outro_individuo)
            i =i+1 # i = i + 1
            # F1 = Q
            population.fronts.append(Qfront)
        return population

    #NSGA-II - calculate crowding distance
    @staticmethod
    def calculate_crowding_distance(front):

        if len(front) > 0:
            # l = I (number of solutions in I)
            solutions = len(front)
            # for each i in I
            for individuo in front:
                # set I[i]distance = 0
                individuo.crowding_distance = 0

                
            # for each objective m
            for fit in range(len(front[0].fitness)):
                # I = sort(I,m) -> Realiza a ordem crescente para cada objetivo
                front.sort(key=lambda individuo: individuo.fitness[fit])
                # I[1]distance = infinit
                front[0].crownding_distance = 10**9
                # I[l]distance = infinit
                front[solutions-1].crowding_distance = 10**9
                fit_values = [individuo.fitness[fit] for individuo in front]
                scale = max(fit_values) - min(fit_values)
                if scale == 0:
                    scale = 1
                # for i = 2 to (l-1)
                for i in range(1, solutions-1):
                    # I[i]distance = I[i]distance + (I[i+1].m - I[i-1].m)/(fmax(m) - fmin(m))
                    front[i].crowding_distance += (front[i+1].fitness[fit] - front[i-1].fitness[fit])/scale
        
        return front

    # NSGA-II - make new population
    @staticmethod
    def make_new_pop(population, macro, model, name_model):
        children = []
        while len(children) < population.size():
            parent1 = Genetic.torneio(population)
            parent2 = parent1
            # Prevent the same individual from winning twice
            while parent1.cromossomo == parent2.cromossomo:
                parent2 = Genetic.torneio(population)
            child = Genetic.crossover(parent1, parent2, macro)
            child = Genetic.mutation(child, macro)
            child = FitnessGurobi.setFitness(macro, model, name_model, child)
            children.append(child)
        return children
