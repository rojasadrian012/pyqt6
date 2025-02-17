from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QTableWidgetItem

from api.productRepository import ProductRepository
from ui.main.components.newProduct.newProduct import NewProduct

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main/main.ui", self)
        self.initUi()
        self.showMaximized()
        self.btnUpdateTable.clicked.connect(self.updateTable)

    def initUi(self):
        self.btnNewProduct.triggered.connect(self.openNewProduct)

    def openNewProduct(self):
        self.newProduct = NewProduct()

    def updateTable(self):
        products = ProductRepository().getAll()
        print(products)
        i = len(products)
        self.tblProducts.setRowCount(i)
        tableRow = 0
        for product in products:
            self.tblProducts.setItem(tableRow, 0, QTableWidgetItem(str(product.name)))
            self.tblProducts.setItem(tableRow, 1, QTableWidgetItem(str(product.description)))
            self.tblProducts.setItem(tableRow, 2, QTableWidgetItem(str(product.category)))
            self.tblProducts.setItem(tableRow, 3, QTableWidgetItem(str(product.price)))
            self.tblProducts.setItem(tableRow, 4, QTableWidgetItem(str(product.isImported)))
            tableRow += 1

