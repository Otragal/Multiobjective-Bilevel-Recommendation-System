# Banco de Dados

Aqui contém o backup do Banco de Dados utilizado para executar o sistema.

Para ver os dados deste banco, é necessário do programa [BD Browser for SQLite](https://sqlitebrowser.org/).

Em `/dietprogram/dabase.py`, é necessário alterar o PATH do banco de dados.

```python

class TacoDB():
    def __init__(self):
        try:
            print("TacoDB::__init__\t Iniciando Banco de Dados")
            # PATH para o Banco de Dados SQLite
            self.path ='/path/do/banco/de/dados/'
            self.database = 'taco4dataset.db'
            self.connect = sqlite3.connect('{url}{db}'.format(url=self.path,db=self.database))
            self.cur = self.connect.cursor()
            print('Conexão criada em '+self.database)
        except sqlite3.Error as error:
            print("Falha em tentar ler os dados no sqlite table ", error)

```