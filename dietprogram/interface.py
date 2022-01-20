import tkinter as tk
from tkinter import Button, messagebox
from tkinter import ttk #combo
from app import App

class Interface:


    def __init__(self):

        # GLOBALS
        self.VALIDE_USER = False

        self.LABEL_CATEGORIA_REF = []
        self.INPUT_CATEGORIA = []
        self.INPUT_CATEGORIA_DATA = [3,3,3,3,3,3]

        self.MATRIZ_CATEGORIA = []
        self.ESTADO = ["Mulher", 4]
        self.IDADE = 0
        self.PORCENTAGEM = 10

        self.FASE = ["Infantil", "Criança", "Homem", "Mulher"]

        self.FASE_VIDA = {
            "Infantil": 1,
            "Criança": 2,
            "Homem": 3,
            "Mulher": 4,
            "Mulher com Gravidez": 5,
            "Mulher com Lactação": 6
        }

        self.NOME_REF = [
            "Café da Manhã",
            "Almoço",
            "Jantar",
            "Lanche Manhã",
            "Lanche Tarde",
            "Pós Janta"
        ]

        self.LISTA_CATEGORIA = ['acucarados','bebidas','carnes',
        'cereais','frutas','gorduras','industrializados',
        'leguminosas','leites','miscelaneas','noezes',
        'ovos','pescados', 'preparados','verduras']

        self.QTD_REF = [2,3,4,5,6]
        self.QTD_REF_DATA = self.QTD_REF[3] # Numero de Refeições
        self.QTD_COMIDA = [0,1,2,3,4,5,6,7,8] 

        
        self.EPOCAS = 10
        self.POVO = 100

        self.root = tk.Tk()
        self.root.title("Sistema de Recomendação de Dieta Alimentar Multiojbetivo")
        self.root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

        self.frame_cardapio = tk.LabelFrame(self.root, text= "Define o Cardápio")
        self.frame_categoria = tk.LabelFrame(self.root, text="Seleciona as Categorias")
        self.startApp()

# DEF
    def callbackInputCategoriaData(self, index, sv):
        print('SV: ' + str(sv.get()))
        print(index)
        return True

    def openUserWindow(self):
        top = tk.Toplevel()
        top.title("Info Usuário")

        #Load FASE_VIDA & ESTADO_VIDA
        vida = tk.StringVar()
        vida.set(self.ESTADO[0])

        tk.Label(top, text="Informações sobre você").grid(row=0, column=0, columnspan=2)
        tk.Label(top, text="Fase de Vida: ").grid(row=1, column=0)
        tk.OptionMenu(top, vida, *self.FASE).grid(row=1, column=1)
        tk.Label(top, text="Idade: ").grid(row=2, column=0)
        idade = tk.Entry(top, width=5, borderwidth=5)
        idade.insert(0, self.IDADE)
        idade.grid(row=2, column=1)
        tk.Label(top, text="anos.",anchor=tk.W).grid(row=2, column=2)
        tk.Label(top, text="Porção dos Alimentos: ").grid(row=3, column=0)
        porcentagem = tk.Entry(top, width=5, borderwidth=5)
        porcentagem.insert(0, self.PORCENTAGEM)
        porcentagem.grid(row=3, column=1)
        tk.Label(top, text="gramas. (Entre 10g e 150g)").grid(row=3, column=2)

        tk.Button(top, text="Cancelar", command=top.destroy).grid(row=4,column=1, columnspan=2)
        tk.Button(top, text="Confirmar", command=lambda: self.validInfoUser(top, vida.get(), idade.get())).grid(row=4,column=0)

    def openSystemWindow(self):
        top = tk.Toplevel()
        top.title("Configuração do Sistema")

        frame_system = tk.LabelFrame(top, text= "NSGA-II")
        tk.Label(top, text = "Número de Épocas: ").grid(row=0, column=0)
        ep = tk.Entry(top, width=10, borderwidth=5)
        ep.insert(0, self.EPOCAS)
        ep.grid(row=0, column=1)
        tk.Label(top, text= "População de Soluções: ").grid(row=1, column=0)
        pv = tk.Entry(top, width=10, borderwidth=5)
        pv.insert(0, self.POVO)
        pv.grid(row=1, column=1)

        tk.Button(top, text="Cancelar", command=top.destroy).grid(row=3,column=1, columnspan=2)
        tk.Button(top, text="Confirmar", command=lambda: self.validInfoSystem(top, ep.get(), pv.get())).grid(row=3,column=0)


    def validInfoUser(self, top, vida, idade):
        if idade.isdigit() and idade != "0":
            self.VALIDE_USER = True
            self.IDADE = int(idade)
        else:
            res = messagebox.showwarning(title="Erro no Campo Idade", message="O valor 'Idade' deve ser somente número")
            self.VALIDE_USER = False
            return
        self.ESTADO = [vida, self.FASE_VIDA[vida]]
        if self.VALIDE_USER:
            top.destroy()
        else:
            return

    def validInfoSystem(self, top, epoca, povo):
        confirm = 0
        if epoca.isdigit() and epoca != "0":
            confirm += 1
            self.EPOCAS = int(epoca)
        else:
            res = messagebox.showwarning(title="Erro na Epoca", message="Digite um valor numérico para definir a quantidade de Épocas")
            self.VALIDE_USER = False
            return
        if povo.isdigit() and povo != "0":
            confirm += 1
            self.POVO = int(povo)
        else:
            res = messagebox.showwarning(title="Erro na População", message="Digite um valor numérico para definir a quantidade da População")
            self.VALIDE_USER = False
            return
        if confirm >= 2:
            top.destroy()
        else:
            res = messagebox.showwarning("Não foi possível alterar a configuração.")
            return


    def updateAlimentos(self,qtd):
        #self.frame_cardapio.grid_forget()
        self.QTD_REF_DATA = int(qtd)
        tk.Label(self.frame_cardapio, text="Quantidade de Refeições: ").grid(row=0, column=0)
        ref = tk.StringVar()
        ref.set(self.QTD_REF_DATA)
        tk.OptionMenu(self.frame_cardapio, ref, *self.QTD_REF, command=self.updateAlimentos).grid(row=0, column=1)
        
        
        print(len(self.INPUT_CATEGORIA))
        # Atualiza e coloca a quantidade de ref no frame
        for i in range(len(self.INPUT_CATEGORIA)):
            self.LABEL_CATEGORIA_REF[i].grid_forget()
            self.INPUT_CATEGORIA[i].grid_forget()
            
        for i in range(self.QTD_REF_DATA):
            self.LABEL_CATEGORIA_REF[i].grid(row=2, column=i)
            self.INPUT_CATEGORIA[i].grid(row=3, column=i)
        
        
        Button(self.frame_cardapio, text="Atualizar o Cardápio", state=tk.ACTIVE, command= self.updateDataAlimentosFromInputs).grid(row=4, column=0)
        self.frame_cardapio.grid(row=1, column=0)

    def updateMatrizCategorias(self):
        for row in range(len(self.MATRIZ_CATEGORIA)):
            for col in range(len(self.MATRIZ_CATEGORIA[row])):
                self.MATRIZ_CATEGORIA[row][col].grid_forget()
        
        for row in range(self.QTD_REF_DATA):
            for col in range(self.INPUT_CATEGORIA_DATA[row]):
                self.MATRIZ_CATEGORIA[row][col].grid(row=col, column=row)

    def setInfoToApp(self):
        print("OKKAY!")

    def getQtdAlimentosFromInputs(self,index, value):
        self.INPUT_CATEGORIA_DATA[index] = value
        
    def updateDataAlimentosFromInputs(self):
        for i in range(len(self.INPUT_CATEGORIA)):
            self.INPUT_CATEGORIA_DATA[i] = int(self.INPUT_CATEGORIA[i].get())

        self.updateMatrizCategorias()
    

        
    def startApp(self):
        
        # Header
        tk.Label(self.root, text="Dieta Alimentar").grid(row=0,column=0)
        tk.Button(self.root, text="Info Usuário", command=self.openUserWindow).grid(row=0, column=2)
        tk.Button(self.root, text="Configuração", command=self.openSystemWindow).grid(row=0, column=3)

    # FRAME CARDAPIO
        # Instanciar os nomes das Refeições no Frame
        for i in range(len(self.NOME_REF)):
            #sv = tk.StringVar()
            #sv.trace_add("write", self.callbackInputCategoriaData(sv))
            #sv.trace("w", lambda name, index, mode, sv=sv: self.callbackInputCategoriaData(sv))
            lb = tk.Label(self.frame_cardapio, text=self.NOME_REF[i])
            self.LABEL_CATEGORIA_REF.append(lb)
            e = tk.Entry(self.frame_cardapio, width=10, borderwidth=2, justify=tk.CENTER)
            e.insert(0, self.INPUT_CATEGORIA_DATA[i])
            # Lista de Inputs de quantidade de cada categoria
            self.INPUT_CATEGORIA.append(e)

        print(self.MATRIZ_CATEGORIA)
        tk.Label(self.frame_cardapio, text="Quantidade de Refeições: ", justify=tk.LEFT).grid(row=0, column=0)
        ref = tk.IntVar()
        ref.set(self.QTD_REF_DATA) # Pega a quantidade de refs
        tk.OptionMenu(self.frame_cardapio, ref, *self.QTD_REF, command=self.updateAlimentos).grid(row=0, column=1)
        
        tk.Label(self.frame_cardapio, text="Quantidade de para cada Refeição:", anchor=tk.E).grid(row=1,column=0)
        # SHOW INPUTS
        for i in range(self.QTD_REF_DATA):
            self.LABEL_CATEGORIA_REF[i].grid(row=2, column=i)
            self.INPUT_CATEGORIA[i].grid(row=3, column=i)

        self.frame_cardapio.grid(row=1, column=0)
        Button(self.frame_cardapio, text="Confirmar o Cardápio", state=tk.ACTIVE, command= self.updateDataAlimentosFromInputs).grid(row=4, column=0)
        self.frame_cardapio.grid(row=1, column=0)

    # FRAME CATEGORIAS
        print(int(self.QTD_REF_DATA))
        for i in range(6):
            categoria_columns = []
            for j in range(15):
                ref = tk.StringVar()
                ref.set(self.LISTA_CATEGORIA[j])
                opt = tk.OptionMenu(self.frame_categoria, ref, *self.LISTA_CATEGORIA)
                categoria_columns.append(opt)
            self.MATRIZ_CATEGORIA.append(categoria_columns)
        
        print(len(self.MATRIZ_CATEGORIA))
        for row in range(self.QTD_REF_DATA):
            for col in range(self.INPUT_CATEGORIA_DATA[row]):
                self.MATRIZ_CATEGORIA[row][col].grid(row=col, column=row)

        self.frame_categoria.grid(row=2,column=0, padx=5, pady=5)


        tk.Button(self.root, text="Buscar as Dietas", command=self.setInfoToApp).grid(row=3, column=0,  padx=5, pady=5)

        tk.mainloop()

Interface()