import sqlite3

class ConnectionRepository():
    def __init__(self):
        try:
            self.con = sqlite3.connect('database/database.db')
        except Exception as e:
            print(e)

    def connexionDatabase(self):
        return self.con
        
