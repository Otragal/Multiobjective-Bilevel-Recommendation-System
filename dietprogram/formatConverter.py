import unicodedata


class FormatConverter:

    @staticmethod
    def getValuesNamesEnergy(cromossomo,porcentagem=None):
        valNuts = []
        varNames = []
        energy = []
        preco = []
        for key, c in enumerate(cromossomo):
            varNames.append(unicodedata.normalize('NFD',c[0].replace(" ",""))+str(key))
            e = c[2] # energia
            p = c[3] # preço
            if porcentagem is not None and porcentagem != 0:
                e = e/porcentagem
                p = p/porcentagem # Define que o Preço é por 100g
            energy.append(e)
            preco .append(p)
            foo = list(c[2:])
            valNuts = [*valNuts, *foo]
        
        varEnergy = dict(dict(zip(varNames,energy)))
        varPreco = dict(dict(zip(varNames, preco)))
        return valNuts, varNames, varEnergy, varPreco

    
    @staticmethod
    def makeDictNutriValues(varNames, nameNuts, valNuts, porcentagem=None):
        print("\nformatConverter::makeDictNutriValues")
        print('VARNAMES:', len(varNames))
        print(varNames)
        print('NAMENUTS:',len(nameNuts))
        print(nameNuts)
        print('VALNUTS:', len(valNuts))
        print(valNuts)
        if porcentagem is not None and porcentagem != 0:
           for i in range(len(valNuts)):
                valNuts[i] = int(valNuts[i])/porcentagem
        keyNut = []
        i =0
        j=0
        for name in varNames:
            for nut in nameNuts:
                tuplaKey = (name,nut)
                keyNut.append(tuplaKey)
        print("KEYNUT:", len(keyNut))
        print(keyNut)
        varNuts = dict(dict(zip(keyNut,valNuts)))
        return varNuts
    
    @staticmethod
    def addOneDictNutrition(nutName, nutValue, constrains):
        constrains[nutName]=nutValue

    @staticmethod
    def makeDictNutrition(nutrition, constrains):
        print('\nformatConverter::makeDictNutrition')
        print('NUTRITION: ','LEN:', len(nutrition))
        print('CONSTRIAINS:',' LEN:',len(constrains))
        print(constrains)
        cons = dict(dict(zip(nutrition,constrains)))
        return cons

    #def makeDictMinNutrition(nutrition, constrains):
    #    minCons = dict(dict(zip(nutrition,constrains)))
    #   return minCons

    