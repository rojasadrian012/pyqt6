from PyQt6.QtWidgets import QApplication
from database.databaseSetup import DatabaseSetup
from ui.login.login import Login


class App():
    def __init__(self):
        DatabaseSetup().verifyAndSetup()     
           
        self.app = QApplication([])
        self.login = Login()
        self.app.exec() 


App()