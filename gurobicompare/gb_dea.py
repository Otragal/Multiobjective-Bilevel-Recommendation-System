
# Example da Tabela 1: A simple linear program with three foods used for diets planned for humans

import gurobipy as gb
from gurobipy import GRB

# Criar um modelo de GUrobi, pois contem os elementos de otimização
model = gb.Model("table1")

# Variáveis

bread = model.addVar(lb=0.0, vtype=GRB.INTEGER, name="Bread")
egg = model.addVar(lb = 0.0, vtype=GRB.INTEGER, name="Egg")
cheese = model.addVar(lb = 0.0, vtype=GRB.INTEGER, name="chesse")

# Função Objetiva com minimização de preço
model.setObjective(0.02*bread + 0.06*egg + 0.062*cheese, GRB.MINIMIZE)

# Restrições
model.addConstr(1*bread + 1*egg + 1*cheese >= 100, "Amount")
model.addConstr(10.37*bread + 6.3*egg + 6.15*cheese >= 1672, "EnergyKJ")
model.addConstr(2.48*bread + 1.5*egg + 1.47*cheese >= 400, "EnergyKCAL")
model.addConstr(0.09*bread + 0.124*egg + 0.15*cheese >= 15, "Protein")

# Otimizar
model.optimize()

# Respostas
for valores in model.getVars():
    print('%s %g' % (valores.varName, valores.x))

print('Obj: %g' % model.objVal)

# Resposta em questão do Preço:
# Bread 167
# Egg -0
# chesse -0
# Obj: 3.34 NIS

# Solução do Paper da Tabela 1
# Bread 113.2
# Eggs 78.7

# O Gurobi apresentou uma solução diferente, mas está próximo a resposta em que a resposta deve comer muito pão.