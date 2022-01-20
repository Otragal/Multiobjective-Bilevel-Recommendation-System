import pandas as pd
import numpy as np
import csv

class Dataset(object):
    def __init__(self):

        dataset = pd.read_excel('TACO4DATASET.xlsx', sheet_name=None)

        self.cereais = dataset['Cereais e derivados']
        self.verduras = dataset['Verduras, hortaliças e derivado']
        self.frutas = dataset['Frutas e derivados']
        self.gorduras_oleos = dataset['Gorduras e óleos']
        self.pescados_frutos_do_mar = dataset['Pescados e frutos do mar']
        self.carnes = dataset['Carnes e derivados']
        self.leites = dataset['Leite e derivados']
        self.bebidas = dataset['Bebidas (alcoólicas e não alcoó']
        self.ovos = dataset['Ovos e derivados']
        self.acucarados = dataset['Produtos açucarados']
        self.miscelaneas = dataset['Miscelâneas']
        self.industrializados = dataset['Outros alimentos industrializad']
        self.preparados = dataset['Alimentos preparados']
        self.leguminosas = dataset['Leguminosas e derivados']
        self.nozes_sementes = dataset['Nozes e sementes']

data = Dataset()


with open('nozes.csv', 'w') as file:
    writer = csv.writer(file, delimiter=';')
    for index, row in data.nozes_sementes.iterrows():
        writer.writerow([row['Nome'], 'Umidade', row['Umidade']])
        writer.writerow([row['Nome'], 'Energia1', row['Energia1']])
        writer.writerow([row['Nome'], 'Energia2', row['Energia2']])
        writer.writerow([row['Nome'], 'Proteina', row['Proteina']])
        writer.writerow([row['Nome'], 'Lipideos', row['Lipideos']])
        writer.writerow([row['Nome'], 'Colesterol', row['Colesterol']])
        writer.writerow([row['Nome'], 'Carboidrato', row['Carboidrato']])
        writer.writerow([row['Nome'], 'FibraAlimentar', row['FibraAlimentar']])
        writer.writerow([row['Nome'], 'Cinzas', row['Cinzas']])
        writer.writerow([row['Nome'], 'Magnesio', row['Magnesio']])
        writer.writerow([row['Nome'], 'Manganes', row['Manganes']])
        writer.writerow([row['Nome'], 'Fosforo', row['Fosforo']])
        writer.writerow([row['Nome'], 'Sodio', row['Sodio']])
        writer.writerow([row['Nome'], 'Potassio', row['Potassio']])
        writer.writerow([row['Nome'], 'Zinco', row['Zinco']])
        writer.writerow([row['Nome'], 'VitaminaA', row['VitaminaA']])
        writer.writerow([row['Nome'], 'RE', row['RE']])
        writer.writerow([row['Nome'], 'RAE', row['RAE']])
        writer.writerow([row['Nome'], 'VitaminaB1', row['VitaminaB1']])
        writer.writerow([row['Nome'], 'VitaminaB2', row['VitaminaB2']])
        writer.writerow([row['Nome'], 'VitaminaB6', row['VitaminaB6']])
        writer.writerow([row['Nome'], 'VitaminaB3', row['VitaminaB3']])
        writer.writerow([row['Nome'], 'VitaminaC', row['VitaminaC']])

print('Done')