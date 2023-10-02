from gurobyModel import GurobiModel
from formatConverter import FormatConverter
import math
import numpy as np

"""       
Class FitnessGurobi()

    Here it works on inserting the Fitness (Objectives) of Individuals
    
    setFitnessPovo()
        it receives the People with its individuals;
        for all individuals:
            converts the individual's information;
            calls the model Gurobi;
            updates the individual's Fitness (Goals);
        returns the People with updated individuals' goals;

    setFitness()
        receives an individual;
        converts the data to acceptable reading;
        calls the model Gurobi;
        updates the individual's Fitness (Goals);
        returns the Individual with updated goals;

    fitnessCustom():
        method that has the equation of DESEMPENHO = Energia + Quantidade + Distribuição + Peso     
"""

class FitnessGurobi():

    @staticmethod
    def setFitnessPovo(macro, model, nome_model, povo):
        for individuo in povo.individuos:
            model = GurobiModel.loadModel(nome_model)
            # Converts to get values, names, energy
            val,name,energy,price = FormatConverter.getValuesNamesEnergy(individuo.cromossomo, macro.porcentagem)
            # Convert to form varNuts
            varNuts = FormatConverter.makeDictNutriValues(name,macro.nutricao,val,macro.porcentagem)
            # Convert to generate mins and max constraints
            minCons = FormatConverter.makeDictNutrition(macro.nutRestricao,macro.restricaoMIN)
            maxCons = FormatConverter.makeDictNutrition(macro.nutRestricao, macro.restricaoMAX)
            # Call Gurobi to do Linear Programming
            model, resultado = GurobiModel.solveCustomModel(model,macro, name, energy, varNuts, maxCons,minCons)

            individuo.setFitness(FitnessGurobi.fitnessCustom(resultado, macro, energy, price))
        return povo

    @staticmethod
    def setFitness(macro, model, nome_model, individuo):
        model = GurobiModel.loadModel(nome_model)
        # Converts to get values, names, energy
        val,name,energy,price = FormatConverter.getValuesNamesEnergy(individuo.cromossomo, macro.porcentagem)    
        # Convert to form varNuts
        varNuts = FormatConverter.makeDictNutriValues(name,macro.nutricao,val,macro.porcentagem)
        # Convert to generate mins and max constraints
        minCons = FormatConverter.makeDictNutrition(macro.nutRestricao, macro.restricaoMIN)
        maxCons = FormatConverter.makeDictNutrition(macro.nutRestricao, macro.restricaoMIN)
        # Call Gurobi to do Linear Programming
        model, resultado = GurobiModel.solveCustomModel(model, macro, name, energy, varNuts, maxCons,minCons)

        individuo.setFitness(FitnessGurobi.fitnessCustom(resultado, macro, energy, price))

        return individuo

    @staticmethod
    def fitnessCustom(resultado, macro, energia, price):
        r = 0
        index = 0
        qtdTotal = 0
        VET = 0
        fit = macro.desempenho
        intervalo = [math.floor(fit.peso_refeicao[0]/2), fit.peso_refeicao[0], fit.peso_refeicao[1], math.floor(fit.peso_refeicao[1]*(1+0.5)), fit.peso_refeicao[1]*2]
        print(intervalo)
        nomes = []
        for key, value in resultado.items():
            qtdTotal += value
            nomes.append(key)
        if macro.porcentagem is not None and macro.porcentagem != 0:
            qtdTotal *=macro.porcentagem

        qtdUnit = list(resultado.values())
        energiaUnit = list(energia.values())
        precoUnit = list(price.values())
        
        # Energia e Custo Total
        VET = float(np.dot(qtdUnit,energiaUnit))
        CUSTO = float(np.dot(qtdUnit,precoUnit))
        #if macro.porcentagem is not None and macro.porcentagem != 0:
        #   CUSTO *=macro.porcentagem

        REFe = []
        REFq = []
        while (r < len(fit.tam_categoria)):
            REFe.append((float(np.dot(qtdUnit[index:(fit.tam_categoria[r]+index)], energiaUnit[index:(fit.tam_categoria[r]+index)]))))
            REFq.append((float(np.sum((qtdUnit[index:(fit.tam_categoria[r]+index)])))))
            index += fit.tam_categoria[r]
            r += 1

        # Desempenho está relacionado a Energia
        pontoEnergia = 0
        # Dempenha a Quantidade
        pontoQuantidade = 0
        # Desempenho a Distribuição
        pontoDistri = 0
        # Desempenho de Peso
        pontoPeso = 0
        
        r = 0
        index = 0
        for i in range(len(REFe)):
            if (REFe[i]/VET)*100 >= (fit.energia_refeicao[i][0]*100) and (REFe[i]/VET)*100 <= (fit.energia_refeicao[i][1]*100):
                pontoEnergia +=1
            if REFq[i] >= fit.quantidade_refeicao[i][0] and REFq[i] <= fit.quantidade_refeicao[i][1]:
                pontoQuantidade += 1
        
        pontoEnergia = pontoEnergia/len(REFe)
        print('Energia = ', pontoEnergia)
        #print('Quantidade = ', pontoQuantidade)
        pontoQuantidade = pontoQuantidade/len(REFq)
        print('Quantidade = ', pontoQuantidade)

        print('qtdTotal = ', qtdTotal)
        #Ponto Peso
        if qtdTotal <= 0:
            pontoPeso = -1
            print(qtdTotal, ' <= ', 0)
        if qtdTotal > 0 and qtdTotal <= intervalo[0]:
            pontoPeso = -(intervalo[0]-qtdTotal)/intervalo[0]
            print(0, ' < ', qtdTotal, ' <= ', intervalo[0])
            print(pontoPeso)
        if qtdTotal > intervalo[0] and qtdTotal < intervalo[1]:
            pontoPeso = (qtdTotal - intervalo[0])/(intervalo[1]-intervalo[0])
            print(intervalo[0], ' < ', qtdTotal, ' <= ', intervalo[1])
            print((qtdTotal - intervalo[0]),' / ', (intervalo[1]-intervalo[0]))
            print(pontoPeso)
        if qtdTotal >= intervalo[1] and qtdTotal <= intervalo[2]:
            pontoPeso = 1
            print(intervalo[1], ' <= ', qtdTotal, ' <= ', intervalo[2])
            print(pontoPeso)
        if qtdTotal > intervalo[2] and qtdTotal <= intervalo[3]:
            pontoPeso = (intervalo[3]-qtdTotal)/(intervalo[3]-intervalo[2])
            print(intervalo[2], ' < ', qtdTotal, ' <=', intervalo[3])
            print((intervalo[3]-qtdTotal), ' / ', (intervalo[3]-intervalo[2]))
            print(pontoPeso)
        if qtdTotal > intervalo[3] and qtdTotal < intervalo[4]:
            pontoPeso = -(qtdTotal-intervalo[3])/(intervalo[4]-intervalo[3])
            print(intervalo[3], ' < ', qtdTotal, ' < ', intervalo[4])
            print(-(qtdTotal-intervalo[3]), ' / ', (intervalo[4]-intervalo[3]))
            print((pontoPeso))
        if qtdTotal >= intervalo[4]:
            pontoPeso = -1
        print('Peso = ', pontoPeso)

        for i in qtdUnit:
            if i > 1.1:
                pontoDistri +=1
        
        #print('Distribução =', pontoDistri)
        pontoDistri = (pontoDistri)/(len(qtdUnit))
        #pontoDistri = (pontoDistri-3)/(len(qtdUnit)-3)
        print('Distribução =', pontoDistri)
        desempenho = -1*(pontoEnergia + pontoQuantidade + pontoDistri + pontoPeso)
        

        print('Quantidade Total = ', qtdTotal, 'g; ou ', qtdTotal/1000, 'Kg')
        print('VET = ', VET, 'kcal')
        print('CUSTO = ', CUSTO, ' reais')
        print('DESEMPENHO = ', desempenho,'de 4 pontos')
        for i in range(len(qtdUnit)):
            print("Nome: %s, Energia: %s, Preço: %s" % (nomes[i], energiaUnit[i], precoUnit[i]))

        print('qtdUnit = ', len(qtdUnit))
        print('energiaUnit = ', len(energiaUnit))
        print('precoUnit = ', len(precoUnit))
        if desempenho < -4.1:
            input("DESEMPENHO >= 4.0...")
            print()
        return [[desempenho, CUSTO],[qtdUnit,energiaUnit,precoUnit]]

    # MÉTODO ANTIGO
    #@staticmethod
    #def fitness(resultado, energia, price, tam_categoria, porcentagem=None):
    #    r = 0
    #    index = 0
    #    qtdTotal = 0
    #    VET = 0
    #    for key, value in resultado.items():
    #        qtdTotal += value
    #    if porcentagem is not None:
    #        qtdTotal /=porcentagem
    #
    #    qtdUnit = list(resultado.values())
    #    energiaUnit = list(energia.values())
    #    precoUnit = list(price.values())
    #    # Energia e Custo Total
    #    VET = float(np.dot(qtdUnit,energiaUnit))
    #    CUSTO = float(np.dot(qtdUnit,precoUnit))
    #    
    #    REFe = []
    #    REFq = []
    #    while (r < len(tam_categoria)):
    #        REFe.append((float(np.dot(qtdUnit[index:(tam_categoria[r]+index)],energiaUnit[index:(tam_categoria[r]+index)]))))
    #        REFq.append((float(np.sum((qtdUnit[index:(tam_categoria[r]+index)])))))
    #        index += tam_categoria[r]
    #        r += 1
    #
    #    # Energia Por Refeição
    #    CMe = float(np.dot(qtdUnit[:3],energiaUnit[:3]))
    #    AJe = float(np.dot(qtdUnit[3:7],energiaUnit[3:7]))
    #    Lae = float(np.dot(qtdUnit[7:],energiaUnit[7:]))
    #    # Quantidade Por Refeição
    #    CMq = float(np.sum((qtdUnit[:3])))
    #    AJq = float(np.sum((qtdUnit[3:7])))
    #    Laq = float(np.sum((qtdUnit[7:])))
    #    
    #    
    #    # Desempenho está relacionado a Energia
    #    pontoEnergia = 0
    #    # Dempenha a Quantidade
    #    pontoQuantidade = 0
    #    # Desempenho a Distribuição
    #    pontoDistri = 0
    #    # Desempenho de Peso
    #    pontoPeso = 0
    #    # Macronutrientes
    #
    #    if (CMe/VET)*100 >= 15.0 and (CMe/VET) <= 35:
    #        pontoEnergia +=1
    #    if (AJe/VET)*100 >= 50 and (AJe/VET)*100 <= 80:
    #        pontoEnergia +=1
    #    if (Lae/VET)*100 >= 5 and (Lae/VET)*100 <= 15:
    #        pontoEnergia +=1
    #    print('Energia = ', pontoEnergia)
    #    pontoEnergia = pontoEnergia/3
    #    print(pontoEnergia)
    #    print(CMq)
    #    print(AJq)
    #    print(Laq)
    #    
    #    if CMq >= 30 and CMq <= 50:
    #        pontoQuantidade +=1
    #    if AJq >= 40 and AJq <= 50:
    #        pontoQuantidade +=1
    #    if Laq >= 30 and Laq <= 50:
    #        pontoQuantidade +=1
    #    print('Quantidade = ', pontoQuantidade)
    #    pontoQuantidade = pontoQuantidade/3
    #    print((pontoQuantidade))
    #    pontoPeso = (qtdTotal - 900)/   (3000 - 900)
    #    if pontoPeso > 0.9:
    #        pontoPeso = 0.9 - (pontoPeso-0.1)
    #    print('Peso = ', pontoPeso)
    #    for i in qtdUnit:
    #        if i > 1.1:
    #            pontoDistri +=1
    #    print('Distribução =', pontoDistri)
    #    pontoDistri = (pontoDistri)/(len(qtdUnit))
    #    #pontoDistri = (pontoDistri-3)/(len(qtdUnit)-3)
    #    print(pontoDistri)
    #    desempenho = -1*(pontoEnergia + pontoQuantidade + pontoDistri + pontoPeso)
    #
    #    print('Quantidade Total = ', qtdTotal, 'g; ou ', qtdTotal/1000, 'Kg')
    #    print('VET = ', VET, 'kcal')
    #    print('CUSTO = ', CUSTO, ' reais')
    #    print('DESEMPENHO = ', desempenho,'de 4 pontos')
    #    print('CM : ', CMe, ', com ', (CMe/VET)*100, '%')
    #    print('A/J : ', AJe, ', com ', (AJe/VET)*100, '%')
    #    print('La : ', Lae, ', com ', (Lae/VET)*100, '%')
    #
    #
    #
    #    return [desempenho, CUSTO]

    # MÉTODO ANTIGO      
    #@staticmethod
    #def bestFitnnes(solutions, energia, price, porcentagem=None):
    #    vResult = []
    #    minQ = [0,999999999]
    #    maxE = [0,0]
    #    minC = [0,999999999]
    #    for index, resultado in solutions:
    #        print(resultado)
    #        qtdTotal = 0
    #        for key, value in resultado.items():
    #            qtdTotal += value
    #        if porcentagem is not None:
    #            qtdTotal /= porcentagem
    #        v1 = list(resultado.values())
    #        v2 = list(energia.values())
    #        v3 = list(price.values())
    #
    #        VET = np.dot(v1,v2)
    #        CUSTO = np.dot(v1,v3)
    #        CM = np.dot(v1[:3],v2[:3])
    #        AJ = np.dot(v1[3:7],v2[3:7])
    #        La = np.dot(v1[7:],v2[7:])
    #        
    #        
    #        pesoRef = 0 
    #        pesoQtd = 0
    #        if qtdTotal <= minQ[1]:
    #            minQ = [index, qtdTotal]
    #        if VET >= maxE[1]:
    #            maxE = [index, VET]
    #        if CUSTO <= minC[1]:
    #            minC = [index, CUSTO]
    #        cm = (CM/VET)*100
    #        if cm >= 15.0 and cm <= 35:
    #            pesoRef += 1
    #        aj = (AJ/VET)*100
    #        if aj >= 50 and aj <= 80:
    #            pesoRef += 1
    #        la = (La/VET)*100
    #        if la >= 5 and la <= 15:
    #            pesoRef += 1
    #        for item in v1:
    #            if item > 1:
    #                pesoQtd +=1
    #        vResult.append([index, 0, pesoRef, pesoQtd])
    #
    #        for index in vResult:
    #            if index[0] == minQ[0]:
    #                index[1] += 1
    #            if index[0] == maxE[0]:
    #                index[1] += 1
    #            if index[0] == minC[0]:
    #                index[0] += 1
                
            
    
