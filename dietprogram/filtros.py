from dataclasses import dataclass

@dataclass
class comida:
    alimento: list
    cromoxomo: list
    categoria: list
    indice: list
    tamanho: int

    def __init__(self, a: list, c: list, i: list):
        self.alimento = a
        self.categoria = c
        self.indice = i
        self.tamanho = len(a)

    def setCromoxomo(self, c:list):
        self.cromoxomo = c

@dataclass
class restricao:
    restriMIN: dict
    restriMAX: dict

    def __init__(self, n: dict, x: dict):
        self.restriMIN = n
        self.restriMAX = x

@dataclass
class desempenho:
    tam_categoria = list
    energia_refeicao = list
    quantidade_refeicao = list
    peso_refeicao = list

    def __init__(self, t:list, e:list, q:list, p:list):
        self.tam_categoria = t
        self.energia_refeicao = e
        self.quantidade_refeicao = q
        self.peso_refeicao = p

@dataclass
class usuario:
    pessoa: int
    idade: int

    def __init__(self, pe:int, i:int, po:int):
        self.pessoa = pe
        self.idade = i

@dataclass
class extras:
    repetir_alimento: bool
    juntar_almoço_jantar: bool
    fixar_alimentos: bool

    def __init__(self, r:bool, j:bool, f:bool):
        self.repetir_alimento = r
        self.juntar_almoço_jantar = j
        self.fixar_alimentos = f