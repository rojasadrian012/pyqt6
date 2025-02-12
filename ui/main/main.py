from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main/main.ui", self)
        self.initUi()
        self.showMaximized()

    def initUi(self):
        self.btnNewProduct.triggered.connect(self.openNewProduct)

    def openNewProduct(self):
        from ui.main.components.newProduct.newProduct import NewProduct
        self.newProduct = NewProduct()
