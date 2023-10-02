# Database

Here contains the backup of the database used to run the system.

To view the data in this database, you will need the [BD Browser for SQLite](https://sqlitebrowser.org/) program.

In `/dietprogram/dabase.py`, it is necessary to change the database PATH.

```python

class TacoDB():
    def __init__(self):
        try:
            print("TacoDB::__init__\t Starting Database")
            # PATH
            self.path ='/path/of/database/'
            self.database = 'taco4dataset.db'
            self.connect = sqlite3.connect('{url}{db}'.format(url=self.path,db=self.database))
            self.cur = self.connect.cursor()
            print('Connection created in '+self.database)
        except sqlite3.Error as error:
            print("Failed to try to read data from sqlite table!", error)

```