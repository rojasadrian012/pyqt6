from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

from api.authRepository import AuthRepository
from model.user import User
from ui.main.main import Main

class Login:
    def __init__(self):
        self.login = uic.loadUi("ui/login/login.ui")
        self.initUi()
        self.login.lblUserError.setStyleSheet("color: red;")
        self.login.lblPasswordError.setStyleSheet("color: red;")
        self.login.show()

    def onLogin(self):
        self.login.lblUserError.setText("")
        self.login.lblPasswordError.setText("")

        user = self.login.txtUser.text()
        password = self.login.txtPassword.text()

        if len(user) < 2:
            self.login.lblUserError.setText("Ingrese un usuario valido.")
            self.login.txtUser.setFocus()
        elif len(password) < 3:
            self.login.lblPasswordError.setText("Ingrese una contraseña válida.")
            self.login.txtPassword.setFocus()
        else:
            user = User(user=user, password=password)
            auth = AuthRepository()
            result = auth.authenticate(user)
            if result:
                self.main = Main()
                self.login.hide()
            else:
                QMessageBox.warning(self.login, "Error", "Usuario o contraseña incorrectos.")

    def initUi(self):
        self.login.btnLogin.clicked.connect(self.onLogin)