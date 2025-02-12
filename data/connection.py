import sqlite3

class Connection():
    def __init__(self):
        try:
            self.con = sqlite3.connect('data/database.db')
            self.createTables()
        except Exception as e:
            print(e)

    def createTables(self):
        sql_create_users = """
            CREATE TABLE IF NOT EXISTS users (
                id integer PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                user TEXT UNIQUE,
                password TEXT
            );
        """
        cursor = self.con.cursor()
        cursor.execute(sql_create_users)

        sql_create_products = """
            CREATE TABLE IF NOT EXISTS products (
                id integer PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                category TEXT,
                price INTEGER,
                isImported BOOLEAN
            );
        """
        cursor.execute(sql_create_products)
        cursor.close()
        self.createUserAdmin()


    def createUserAdmin(self):
        try:
            sql_create_admin_user = """ 
                INSERT OR IGNORE INTO users (name, user, password) 
                VALUES ('Admin', 'admin', 'admin');
            """
            cursor = self.con.cursor()
            cursor.execute(sql_create_admin_user)
            self.con.commit()
        except Exception as e:
            print("Error al crear el usuario admin:", e)


    def connectDatabase(self):
        return self.con
        
