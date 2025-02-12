from PyQt6.QtWidgets import QApplication
from ui.login.login import Login

class App():
    def __init__(self):
        self.app = QApplication([])
        self.login = Login()
        self.app.exec() 


App()