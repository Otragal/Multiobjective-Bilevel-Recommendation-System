import os
import sqlite3

class TacoDB():
    def __init__(self):
        try:
            print("TacoDB::__init__\t Iniciando Banco de Dados")
            # PATH para o Banco de Dados SQLite
            self.path ='/home/otragal/Workspace/sqliteDatabases/'
            self.database = 'taco4dataset.db'
            self.connect = sqlite3.connect('{url}{db}'.format(url=self.path,db=self.database))

            self.cur = self.connect.cursor()

            print('Conexão criada em '+self.database)
        except sqlite3.Error as error:
            print("Falha em tentar ler os dados no sqlite table ", error)

    def selectCategoria(self,tabela, query):
        sqlite_select_query = '''SELECT Nome, Id, ''' +''', '''.join(query) + ''' FROM {}'''.format(tabela)
        #print(sqlite_select_query)
        #sqlite_select_query = '''SELECT Nome, Energia1, Proteina, Calcio, FibraAlimentar FROM {}'''.format(tabela)
        self.cur.execute(sqlite_select_query)
        select = self.cur.fetchall()
        print('TacoBD::selectCategoria\t Select FROM {} efetuado'.format(tabela))
        return select

    def selectConstrainMIN(self, usu, rMin):
        sqlite_select_query = '''SELECT '''+''', '''.join(rMin)+''' FROM restricoes WHERE Pessoas_id = {} AND Idade >= {}'''.format(usu.pessoa, usu.idade)
        #sqlite_select_query = '''SELECT ProteinaMIN, CalcioMIN, FibraAlimentarMIN FROM restricoes WHERE Pessoas_id = {} and Idade >= {}'''.format(id, idade)
        self.cur.execute(sqlite_select_query)
        select = self.cur.fetchall()
        print('TacoDB::selectConstrainMIN\t Select FROM restruicoes efetuado no ID {} e Idade {}'.format(usu.pessoa, usu.idade))
        return select[0] 
    
    def selectConstrainMAX(self, usu, rMax):
        sqlite_select_query = '''SELECT '''+''', '''.join(rMax)+''' FROM restricoes WHERE Pessoas_id = {} AND Idade >= {}'''.format(usu.pessoa, usu.idade)
        #sqlite_select_query = '''SELECT ProteinaMAX, CalcioMAX, FibraAlimentarMAX FROM restricoes WHERE Pessoas_id = {} and Idade >= {}'''.format(id, idade)
        self.cur.execute(sqlite_select_query)
        select = self.cur.fetchall()
        print('TacoDB::selectConstrainMAX\t Select FROM restruicoes efetuado no ID {} e Idade {}'.format(usu.pessoa, usu.idade))
        print(select)
        return select[0]


    def selectOneFood(self, comida, tabela, query):
        sqlite_select_query = '''SELECT Nome, Id, ''' +''', '''.join(query) + ''' FROM {} WHERE Nome = "{}"'''.format(tabela, comida)
        self.cur.execute(sqlite_select_query)
        select = self.cur.fetchall()
        print('Genetic::selectOneFood\t Select {} FROM {} efetuado'.format(comida, tabela))
        return select[0]

    def selectRandomFood(self, tabela, query):
        sqlite_select_query = '''SELECT Nome, Id, ''' +''', '''.join(query) + ''' FROM {} ORDER BY RANDOM()'''.format(tabela)
        self.cur.execute(sqlite_select_query)
        select = self.cur.fetchall()
        print('TacoDB::selectRandomFood\t Select FROM {} efetuado'.format(tabela))
        return select[0]

    def selectRandomRestrictFood(self, tabela, id, query):
        sqlite_select_query = '''SELECT Nome, Id, ''' + ''', '''.join(query) + ''' FROM {} WHERE Id NOT IN ({}) ORDER BY RANDOM()'''.format(tabela,id)
        self.cur.execute(sqlite_select_query)
        select = self.cur.fetchall()
        print('TacoDB::selectRandomRestrictFood\t Select FROM {} efetuado'.format(tabela))
        return select[0]

    def quit(self):
        print('TacoDB:quit\t Desconectando com {}'.format(self.database))
        self.cur.close()
        print('SQLite3 Desconectado')
        return 0
         

# sqlite_select_query, retorna uma lista de tuplas


#    def readSQLite():
#        
#            path = '/home/ancalangon/Workspace/sqliteDatabases/taco4dataset.db'
#            conn = sqlite3.connect(path)
#            cur = conn.cursor()
#            print('Sucesso em Conectar SQLite')
#
#            sqlite_select_query = '''SELECT Nome, Proteina, Calcio, Sodio, Ferro, VitaminaA FROM Cereais'''
#
#            cur.execute(sqlite_select_query)
#            select = cur.fetchall()
#            print(select)
#            conn.close()
#
#
#
#        
#        finally:
#            if (conn):
#                conn.close()
#                print("SQLite desconectou")

#db = TacoDB()
#tabela = 'Cereais'
#cereal = db.selectQuery(tabela)
#primeiraLista = cereal[0]
#print(cereal.type())
#db.quit()