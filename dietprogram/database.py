import os
import sqlite3

class TacoDB():
    def __init__(self):
        try:
            print("TacoDB::__init__\t Starting Database")
            # PATH para o Banco de Dados SQLite
            self.path ='/home/otragal/Workspace/sqliteDatabases/'
            self.database = 'taco4dataset.db'
            self.connect = sqlite3.connect('{url}{db}'.format(url=self.path,db=self.database))

            self.cur = self.connect.cursor()

            print('Connection created in '+self.database)
        except sqlite3.Error as error:
            print("Failed to try to read data from sqlite table!", error)

    def selectCategoria(self,tabela, query):
        sqlite_select_query = '''SELECT Nome, Id, ''' +''', '''.join(query) + ''' FROM {}'''.format(tabela)
        self.cur.execute(sqlite_select_query)
        select = self.cur.fetchall()
        print('TacoBD::selectCategoria\t Select FROM {} accomplished.'.format(tabela))
        return select

    def selectConstrainMIN(self, usu, rMin):
        sqlite_select_query = '''SELECT '''+''', '''.join(rMin)+''' FROM restricoes WHERE Pessoas_id = {} AND Idade >= {}'''.format(usu.pessoa, usu.idade)
        self.cur.execute(sqlite_select_query)
        select = self.cur.fetchall()
        print('TacoDB::selectConstrainMIN\t Select FROM restruicoes accomplished by ID {} and Idade {}'.format(usu.pessoa, usu.idade))
        return select[0] 
    
    def selectConstrainMAX(self, usu, rMax):
        sqlite_select_query = '''SELECT '''+''', '''.join(rMax)+''' FROM restricoes WHERE Pessoas_id = {} AND Idade >= {}'''.format(usu.pessoa, usu.idade)
        self.cur.execute(sqlite_select_query)
        select = self.cur.fetchall()
        print('TacoDB::selectConstrainMAX\t Select FROM restruicoes accomplished by ID {} and Idade {}'.format(usu.pessoa, usu.idade))
        return select[0]


    def selectOneFood(self, comida, tabela, query):
        sqlite_select_query = '''SELECT Nome, Id, ''' +''', '''.join(query) + ''' FROM {} WHERE Nome = "{}"'''.format(tabela, comida)
        self.cur.execute(sqlite_select_query)
        select = self.cur.fetchall()
        print('Genetic::selectOneFood\t Select {} FROM {} accomplished'.format(comida, tabela))
        return select[0]

    def selectRandomFood(self, tabela, query):
        sqlite_select_query = '''SELECT Nome, Id, ''' +''', '''.join(query) + ''' FROM {} ORDER BY RANDOM()'''.format(tabela)
        self.cur.execute(sqlite_select_query)
        select = self.cur.fetchall()
        print('TacoDB::selectRandomFood\t Select FROM {} accomplished'.format(tabela))
        return select[0]

    def selectRandomRestrictFood(self, tabela, id, query):
        sqlite_select_query = '''SELECT Nome, Id, ''' + ''', '''.join(query) + ''' FROM {} WHERE Id NOT IN ({}) ORDER BY RANDOM()'''.format(tabela,id)
        self.cur.execute(sqlite_select_query)
        select = self.cur.fetchall()
        print('TacoDB::selectRandomRestrictFood\t Select FROM {} accomplished'.format(tabela))
        return select[0]

    def quit(self):
        print('TacoDB:quit\t Disconnecting with {}'.format(self.database))
        self.cur.close()
        print('SQLite3 Disconnected')
        return 0
         