import unicodedata

"""       
Class FormatConvert()

    Here it converts the data into correct formats for the Gurobi model

    getValuesNamesEnergy()
        creates two lists (nutrients and nutrient names), and two dictionaries (energy and nutrients) of an individual's chromosome
        
        for each chromosome genome:
            puts all the names of the foods in a list;
            if it has a varied portion, apply energy and food prices to the values;
            enter energy values and food prices and add them to the respective lists;
            creates the energy {food_name: energy_value} and price {food_name: price_value} dictionaries;
        returns valNuts, varNames, varEnergy, varPreco;

    makeDictNutriValues()
        creates a nutrient dictionary in which nutrient values must correlate with the keys formed in pairs (food_name and nutrient_name).

    addOneDictNutrition():
        add a new user-given restriction

    makeDictNutrition():
        creates a constrain dictionary of nutrients and constrains
             
"""

class FormatConverter:

    @staticmethod
    def getValuesNamesEnergy(cromossomo,porcentagem=None):
        valNuts = []
        varNames = []
        energy = []
        preco = []
        for key, c in enumerate(cromossomo):
            varNames.append(unicodedata.normalize('NFD',c[0].replace(" ",""))+str(key))
            # c:
            # c[0] = name
            # c[1] = id
            # c[2] = energy (objective 1)
            # c[3] = price (price 2)
            e = c[2] 
            p = c[3] 
            if porcentagem is not None and porcentagem != 0:
                e = e/porcentagem
                p = p/porcentagem # Defines that the Price is per 100g
            energy.append(e)
            preco .append(p)
            # get all elements of c[2:], that is, energy values
            foo = list(c[2:])
            # concatena a lista "foo" com a lista existente 'valNuts", resultando uma lista combinada de "valNuts"
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
        # The result of two loops is that "keyNut" will contain all possible combinations of "varNames" and "nameNuts" elements.
        for name in varNames:
            for nut in nameNuts:
                tuplaKey = (name,nut)
                keyNut.append(tuplaKey)
        # combines "jeyNut" and "valNuts"
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



    