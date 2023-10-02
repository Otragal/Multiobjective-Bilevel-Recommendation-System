import gurobipy as gp
from gurobipy import GRB


"""
Class GurobiModel:

    Contains the GUROBI model (needs gurobi license)

    createModel()
        Method that creates the Gurobi Model and saves the model with name "name";

    loadModel()
        Method that loads save file from Gurobi Model;

    solveCustomModel()
        Method that has Gurobi's linear model;
        performs multiple saves;
        returns the results;

    printSolution()
        Method that prints the results of the model in the terminal;

"""

class GurobiModel:
    
    @staticmethod                
    def createModel(name):
        print("Creating Model Gurabi '{}'".format(name))
        model = gp.Model(name)
        model.write('{}.mps'.format(name))
        print("Model {}.mps created".format(name))
        return model

    @staticmethod
    def loadModel(name):
        print('Searching Model {}.mps'.format(name))
        try:
            model = gp.read('{}.mps'.format(name))
            return model
        except IOError as exc:
            raise RuntimeError('Unable to load model') from exc
        
        finally:
            print('Loading ended')    
        
    @staticmethod
    def solveCustomModel(model, macro, variables, objective, valuesConstrains, maxConstrains, minConstrains=None):
        # macro variables
        constrains = macro.nutRestricao
        tam_grupo = macro.desempenho.tam_categoria
        energia_distri = macro.desempenho.energia_refeicao
        macronutriente = macro.macronutriente

        # account variables
        r = 0
        index = 0
        model.Params.LogToConsole = 0

        # Create decision variables
        quantidade = {}
        for v in variables:
            quantidade[v] = model.addVar(lb=1.0, ub=151.0, vtype=GRB.INTEGER, name=v)

        z = sum(quantidade[v]*objective[v] for v in variables)

        # Defining the objective would be to maximize
        model.setObjective(z, GRB.MAXIMIZE)
        

        # Set the restrictions:
        #   Minimum Energy Constraints
        model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables) >= 2400),'Energia')
        #   Cost Constraint
        model.addConstr((gp.quicksum(valuesConstrains[v,'Preco']*quantidade[v] for v in variables) <= 500),'Preco')
        #   Others Constraints
        model.addConstrs((gp.quicksum(valuesConstrains[v, c]*quantidade[v] for v in variables) >= minConstrains[c] for c in constrains),'MinCons')
        model.addConstrs((gp.quicksum(valuesConstrains[v, c]*quantidade[v] for v in variables) <= maxConstrains[c] for c in constrains),'MaxCons')
        
        while (r < len(tam_grupo)):
            model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[index:(tam_grupo[r]+index)]) >= z*(energia_distri[r][0])),'_Ener_Min')
            model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables[index:(tam_grupo[r]+index)]) <= z*(energia_distri[r][1])),'_Ener_Max')
            index += tam_grupo[r]
            r += 1

        while ( r < macronutriente.tamanho):
            model.addConstr((gp.quicksum(valuesConstrains[ v, macronutriente.nomes_macro[i] ]*quantidade[v] for v in variables) >= z*(macronutriente[i][0])), '_MacroNutre_Min')
            model.addConstr((gp.quicksum(valuesConstrains[ v, macronutriente.nomes_macro[i] ]*quantidade[v] for v in variables) <= z*(macronutriente[i][1])), '_MacroNutre_Min')
            r += 1
        
    
        # Solve Model
        model.optimize()
        model.write('model_optimize.mps') # Save
        if model.solCount == 0 or model.status == GRB.INFEASIBLE:
            print("O modelo feito é Inviável")
            model.computeIIS()
            model.write("model_problem_iis.ilp") # Model Infeasble Save
            model.feasRelaxS(0, True, False, True)
            model.optimize() 
        model.write('final_model_optimize.mps') # Final Model Save

        nSolutions = model.SolCount
        nObjectives = model.NumObj
        print('Number of Solutions: ', nSolutions)
        print('Number of Objectives: ', nObjectives)

        solution = GurobiModel.giveSolution(model, len(variables))
        # PRINT
        GurobiModel.printSolution(model)
        
        return model, solution


    @staticmethod
    def printSolution(model):            
        # To report results
        #   Objective function:
        print('Obj: %g' % model.objVal)
        #   Values
        for valores in model.getVars():
            print('%s %g' % (valores.varName, valores.x))



"""
>>>>>>>>>>>>>>>> TESTING METHODS

    The methods below are test methods, they were used to test several Gurobi models.
    The solveCustomModel() method is the final result after all tests.

    They were used to try how to use the Gurobi library.
    They are not working correctly, but they offer interesting examples of how to use the gurobi library in Python

    solveModel() was used to understand the addition of constraints;
    solveMultiModel() was used to understand how to create a solver with two objective functions;

"""


    @staticmethod
    def solveModel(model, constrains, variables, objective, valuesConstrains, maxConstrains, minConstrains=None):

        # Create decision variables
        #   Its possible to create this way:
        #quantidade = model.addVars(variables, name="Comida")

        #   Or this way:
        quantidade = {}
        for v in variables:
            quantidade[v] = model.addVar(lb=1.0, ub=151.0, vtype=GRB.INTEGER, name=v)

        z = sum(quantidade[v]*objective[v] for v in variables)
        # Objective Function
        #   Its possible to set  
        #model.setObjective(quantidade.prod(objective), GRB.MINIMIZE)
        #   Or by this
        model.setObjective(z, GRB.MINIMIZE)

        # Set the restrictions
        #   One of the manual ways to create restrictions:
        if minConstrains is not None:
            
            # Minimum Power Constraints
            model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables) >= 2000),'Energia')
            # Cost Constraint
            model.addConstr((gp.quicksum(valuesConstrains[v,'Preco']*quantidade[v] for v in variables) <= 500),'Proteina')
            # Other Constraints
            model.addConstrs((gp.quicksum(valuesConstrains[v, c]*quantidade[v] for v in variables) >= minConstrains[c] for c in constrains),'MinCons')
            model.addConstrs((gp.quicksum(valuesConstrains[v, c]*quantidade[v] for v in variables) <= maxConstrains[c] for c in constrains),'MaxCons')
            
            # Maximum Energy Restriction
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

        # Create decision variables
        quantidade = {}
        for v in variables:
            quantidade[v] = model.addVar(lb=1.0, ub=100.0, vtype=GRB.INTEGER, name=v)

        # Set Priorities: VET = 2.0 e CUSTO = 1
        SetObjPriority = [2, 1]
        # Define the Weights of each Objective: VET =1.0 e CUSTO -1.0
        # In the MINIMIZE Document, the weight must be negative
        SetObjWeight = [1.0, -1.0]
        # Defining the objective would be to maximize
        model.ModelSense = GRB.MAXIMIZE

        # Defines how many solutions can be in the collection
        model.setParam(GRB.Param.PoolSolutions, 100)

        # Configure the model that will have two objectives
        # Objective 0: VET
        objn = sum(quantidade[v]*objective1[v] for v in variables)
        model.setObjectiveN(objn, 0, SetObjPriority[0], SetObjWeight[0], 1.0+0, 0.01, 'VET')
        # Objective 1: CUSTO
        objn = sum(quantidade[v]*objective2[v] for v in variables)
        model.setObjectiveN(objn, 1, SetObjPriority[1], SetObjWeight[1], 1.0+1, 0.01, 'CUSTO')
        # Set the restrictions
        if minConstrains is not None:
            
            # Energy Constraints
            model.addConstr((gp.quicksum(valuesConstrains[v,'Energia1']*quantidade[v] for v in variables) >= 2000),'Energia')
            # Cost Constraint
            model.addConstr((gp.quicksum(valuesConstrains[v,'Preco']*quantidade[v] for v in variables) <= 500),'Preco')
            # Other Constraints
            model.addConstrs((gp.quicksum(valuesConstrains[v, c]*quantidade[v] for v in variables) >= minConstrains[c] for c in constrains),'MinCons')
            model.addConstrs((gp.quicksum(valuesConstrains[v, c]*quantidade[v] for v in variables) <= maxConstrains[c] for c in constrains),'MaxCons')
            
            # Quantity Restriction
            #model.addConstrs((quantidade[v] >= 1 for v in variables),'Qtd_Min')
            
            model.addConstr((gp.quicksum(quantidade[v] for v in variables[:3]) <= 40),'CM')
            model.addConstr((gp.quicksum(quantidade[v] for v in variables[4:7]) <= 70),'A/J')
            model.addConstr((gp.quicksum(quantidade[v] for v in variables[7:]) <= 40),'La')

            # Maximum Energy Restriction
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

"""

    Other ancient methods of presenting solutions and answers

"""

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