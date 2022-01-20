import gurobipy as gp
from gurobipy import GRB


"""
Class GurobiModel:

    Contém o modelo GUROBI

    createModel()
        Método que cria o Gurobi Model e salva o modelo com nome "name"

    loadModel()
        Método que carrega o arquivo salve do Gurobi Model

    solveCustomModel()
        Método que tem o modelo linear do Gurobi
        realiza vários salvamentos
        retorna os resultados

    printSolution()
        Método que print no terminal os resultados do modelo

"""

class GurobiModel:
    
    @staticmethod                
    def createModel(name):
        print("Criando Model Gurabi '{}'".format(name))
        model = gp.Model(name)
        model.write('{}.mps'.format(name))
        print("Model {}.mps criado".format(name))
        return model

    @staticmethod
    def loadModel(name):
        print('Procurando Model {}.mps'.format(name))
        try:
            model = gp.read('{}.mps'.format(name))
            return model
        except IOError as exc:
            raise RuntimeError('Não foi possível carregar o model') from exc
        
        finally:
            print('Carregamento encerrado')    
        
    @staticmethod
    def solveCustomModel(model, macro, variables, objective, valuesConstrains, maxConstrains, minConstrains=None):
        #variabeis de macro
        constrains = macro.nutRestricao
        tam_grupo = macro.desempenho.tam_categoria
        energia_distri = macro.desempenho.energia_refeicao

        #variaveis de conta
        r = 0
        index = 0
        
        model.Params.LogToConsole = 0

        quantidade = {}
        for v in variables:
            quantidade[v] = model.addVar(lb=1.0, ub=151.0, vtype=GRB.INTEGER, name=v)

        z = sum(quantidade[v]*objective[v] for v in variables)
        # Defenir o objectio, seria Maximizar
        #model.setObjective(quantidade.prod(objective), GRB.MINIMIZE)
        model.setObjective(z, GRB.MAXIMIZE)
        # Definir as restrições

        # Restrições de Energia Minima
        model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables) >= 2000),'Energia')
        # Restrição de Custo
        model.addConstr((gp.quicksum(valuesConstrains[v,'Preco']*quantidade[v] for v in variables) <= 500),'Preco')
        # Restrições
        model.addConstrs((gp.quicksum(valuesConstrains[v, c]*quantidade[v] for v in variables) >= minConstrains[c] for c in constrains),'MinCons')
        model.addConstrs((gp.quicksum(valuesConstrains[v, c]*quantidade[v] for v in variables) <= maxConstrains[c] for c in constrains),'MaxCons')
        
        
        #for (key, value) in set(tam_grupo.items()) & set(energia_distri.items()):
        #    limite = energia_distri(key)
        #    tam = tam_grupo(key)

        while (r < len(tam_grupo)):
            model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[index:(tam_grupo[r]+index)]) >= z*(energia_distri[r][0])),'_Min')
            model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[index:(tam_grupo[r]+index)]) <= z*(energia_distri[r][1])),'_Max')
            index += tam_grupo[r]
            r += 1
        
        # Solve Model
        model.optimize()
        model.write('model_optimize.mps') # Salva
        if model.solCount == 0 or model.status == GRB.INFEASIBLE:
            print("O modelo feito é Inviável")
            model.computeIIS()
            model.write("model_problem_iis.ilp") # Model Infactivo Salva
            model.feasRelaxS(0, True, False, True)
            model.optimize() 
        model.write('final_model_optimize.mps') # Model Final Salva

        nSolutions = model.SolCount
        nObjectives = model.NumObj
        print('Numero de Soluções: ', nSolutions)
        print('Numero de Objetivos: ', nObjectives)

        solution = GurobiModel.giveSolution(model, len(variables))
        # PRINT
        GurobiModel.printSolution(model)
        
        return model, solution


    @staticmethod
    def printSolution(model):            
        # Para reportar os resultados
        #   Função objetivo:
        print('Obj: %g' % model.objVal)
        #   Valores
        for valores in model.getVars():
            print('%s %g' % (valores.varName, valores.x))


# >>>>>>>>>>>>>>>> MÉTODOS DE TESTES

    @staticmethod
    def solveModel(model, constrains, variables, objective, valuesConstrains, maxConstrains, minConstrains=None):

        # Criar variaveis de decisões
        #quantidade = model.addVars(variables, name="Comida")
        quantidade = {}
        for v in variables:
            quantidade[v] = model.addVar(lb=1.0, ub=151.0, vtype=GRB.INTEGER, name=v)

        z = sum(quantidade[v]*objective[v] for v in variables)
        # Defenir o objectio, seria Maximizar
        #model.setObjective(quantidade.prod(objective), GRB.MINIMIZE)
        model.setObjective(z, GRB.MINIMIZE)
        # Definir as restrições
        if minConstrains is not None:
            
            # Restrições de Energia Minima
            model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables) >= 2000),'Energia')
            # Restrição de Custo
            model.addConstr((gp.quicksum(valuesConstrains[v,'Preco']*quantidade[v] for v in variables) <= 500),'Preco')
            # Restrições
            model.addConstrs((gp.quicksum(valuesConstrains[v, c]*quantidade[v] for v in variables) >= minConstrains[c] for c in constrains),'MinCons')
            model.addConstrs((gp.quicksum(valuesConstrains[v, c]*quantidade[v] for v in variables) <= maxConstrains[c] for c in constrains),'MaxCons')
            # Restrição Máxima de Energia
            #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables) == z), 'Energia Total')
            model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[:3]) >= z*0.15),'CM_Min')
            model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[:3]) <= z*0.35),'CM_Max')
            model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[3:7]) >= z*0.50),'AJ_Min')
            model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[3:7]) <= z*0.80),'AJ_Max')
            model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[7:]) >= z*0.05),'La_Min')
            model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[7:]) <= z*0.15),'La_Max')
            #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables) <= maxConstrains['Energia']),'Energia100')
        else:
            model.addConstrs((gp.quicksum(valuesConstrains[v, c]*quantidade[v] for v in variables) <= maxConstrains[c] for c in constrains))


        # Solve
        model.optimize()
        model.write('teste3.mps')
        if model.solCount == 0 or model.status == GRB.INFEASIBLE:
            print("O modelo feito é Inviável")
            model.computeIIS()
            model.write("diet_iis.ilp")
            model.feasRelaxS(0, True, False, True)
            model.optimize()
        model.write('teste4.mps')

        #obj = math.ceil(model.objVal)
        ## Restrição Máxima de Energia
        #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[:3]) >= obj*0.15),'CM_Min')
        #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[:3]) <= obj*0.35),'CM_Max')
        #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[3:7]) >= obj*0.50),'AJ_Min')
        #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[3:7]) <= obj*0.80),'AJ_Max')
        #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[7:]) >= obj*0.05),'La_Min')
        #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[7:]) <= obj*0.15),'La_Max')
        #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables) <= maxConstrains['Energia1']),'Energia100')

        nSolutions = model.SolCount
        nObjectives = model.NumObj
        print('Numero de Soluções: ', nSolutions)
        print('Numero de Objetivos: ', nObjectives)

        solution = GurobiModel.giveSolution(model, len(variables))
        # PRINT
        GurobiModel.printSolution(model)
        
        return model, solution

    @staticmethod
    def solveMultiModel(model, constrains, variables, objective1, objective2, valuesConstrains, maxConstrains, minConstrains=None):

        # Criar variaveis de decisões
        #quantidade = model.addVars(variables, name="Comida")
        quantidade = {}
        for v in variables:
            quantidade[v] = model.addVar(lb=1.0, ub=100.0, vtype=GRB.INTEGER, name=v)

        # Definir as Prioridades: VET = 2.0 e CUSTO = 1
        SetObjPriority = [2, 1]
        # Definir os Pesos de cada Objetivo: VET =1.0 e CUSTO -1.0
        # No Documento para MINIMIZAR, o peso deve estar negativo
        SetObjWeight = [1.0, -1.0]
        # Defenir o objectio, seria Maximizar
        model.ModelSense = GRB.MAXIMIZE

        # Define quantas soluções podem ter na coleta
        model.setParam(GRB.Param.PoolSolutions, 100)

        # Configurar o modelo que terá dois objetivos
        # Objetivo 0: VET
        objn = sum(quantidade[v]*objective1[v] for v in variables)
        model.setObjectiveN(objn, 0, SetObjPriority[0], SetObjWeight[0], 1.0+0, 0.01, 'VET')
        # Objetivo 1: CUSTO
        objn = sum(quantidade[v]*objective2[v] for v in variables)
        model.setObjectiveN(objn, 1, SetObjPriority[1], SetObjWeight[1], 1.0+1, 0.01, 'CUSTO')
        # Definir as restrições
        if minConstrains is not None:
            
            # Restrições de Energia
            model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables) >= 2000),'Energia')
            # Restrição de Custo
            model.addConstr((gp.quicksum(valuesConstrains[v,'Preco']*quantidade[v] for v in variables) <= 500),'Preco')
            # Restrições
            model.addConstrs((gp.quicksum(valuesConstrains[v, c]*quantidade[v] for v in variables) >= minConstrains[c] for c in constrains),'MinCons')
            model.addConstrs((gp.quicksum(valuesConstrains[v, c]*quantidade[v] for v in variables) <= maxConstrains[c] for c in constrains),'MaxCons')
            
            # Restrição de Quantidade
            #model.addConstrs((quantidade[v] >= 1 for v in variables),'Qtd_Min')
            
            model.addConstr((gp.quicksum(quantidade[v] for v in variables[:3]) <= 40),'CM')
            model.addConstr((gp.quicksum(quantidade[v] for v in variables[4:7]) <= 70),'A/J')
            model.addConstr((gp.quicksum(quantidade[v] for v in variables[7:]) <= 40),'La')

            # Restrição Máxima de Energia
            #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[:3]) >= minConstrains['Energia1']*0.15),'CM_Min')
            #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[:3]) <= minConstrains['Energia1']*0.35),'CM_Max')
            #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[3:7]) >= minConstrains['Energia1']*0.50),'AJ_Min')
            #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[3:7]) <= minConstrains['Energia1']*0.80),'AJ_Max')
            #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[7:]) >= minConstrains['Energia1']*0.05),'La_Min')
            #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[7:]) <= minConstrains['Energia1']*0.15),'La_Max')
            #model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables) <= maxConstrains['Energia']),'Energia100')
        else:
            model.addConstrs((gp.quicksum(valuesConstrains[v, c]*quantidade[v] for v in variables) <= maxConstrains[c] for c in constrains))

   
        # Solve
        model.write('multiobj.lp')

        # Optimize
        model.optimize()
        model.setParam(GRB.Param.OutputFlag, 0)

        # Status checking
        status = model.Status
        if status in (GRB.INF_OR_UNBD, GRB.INFEASIBLE, GRB.UNBOUNDED):
            print("The model cannot be solved because it is infeasible or "
                  "unbounded")
            model.computeIIS()
            model.write("diet_iis.ilp")
            model.feasRelaxS(0, True, False, True)
            model.optimize()

        if status != GRB.OPTIMAL:
            print('Optimization was stopped with status ' + str(status))
            
        solutions = []
        nSolutions = model.SolCount
        nObjectives = model.NumObj
        print('Numero de Soluções: ', nSolutions)
        print('Numero de Objetivos: ', nObjectives)

        # Print best selected set
        print('Selected elements in best solution:')
        selected = [v for v in variables if quantidade[v].X > 0.9]
        print(" ".join("El{}".format(v) for v in selected))

        # Print number of solutions stored
        nSolutions = model.SolCount
        print('Number of solutions found: ' + str(nSolutions))

        # Print objective values of solutions
        if nSolutions > 10:
            nSolutions = 10
        print('Objective values for first ' + str(nSolutions) + ' solutions:')
        for i in range(1):
            model.setParam(GRB.Param.ObjNumber, i)
            objvals = []
            for e in range(nSolutions):
                model.setParam(GRB.Param.SolutionNumber, e)
                objvals.append(model.ObjNVal)

        print('\tSet{} {:6g} {:6g} {:6g}'.format(i, *objvals))


        return model



    @staticmethod
    def separateSolutions(model, tamanho, nSolutions):
        solution = []
        for n in range(nSolutions):
            model.setParam(GRB.Param.SolutionNumber, n)
            valores = model.getVars()
            resName = []
            resVal = []
            for i in range(tamanho):
                resName.append(valores[i].varName)
                resVal.append(valores[i].x)
            solution.append(dict(zip(resName,resVal)))

    @staticmethod
    def giveSolution(model,tamanho):
        resName = []
        resVal = []
        valores = model.getVars()
        for i in range(tamanho):
            resName.append(valores[i].varName)
            resVal.append(valores[i].x)
        return dict(zip(resName,resVal))