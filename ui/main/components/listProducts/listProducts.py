from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QTableWidgetItem
import pyqtgraph as pg
import numpy as np

from api.productRepository import ProductRepository
from ui.main.components.viewProduct.viewProduct import ViewProduct

class ListProducts:
    def __init__(self):
        self.listProducts = uic.loadUi("ui/main/components/listProducts/listProducts.ui")
        self.initUi()
        self.getProducts()
        self.listProducts.show()

    def initUi(self):
        self.listProducts.btnUpdateTable.clicked.connect(self.getProducts)
        self.listProducts.qleSearch.textChanged.connect(self.filterTable) 
        self.listProducts.tblProducts.setSortingEnabled(True)
        self.listProducts.tblProducts.cellDoubleClicked.connect(self.openDetailProduct)

    def getProducts(self):
        self.products = ProductRepository().getAll()  # Obtenemos la lista completa
        self.populateTable(self.products)

    def populateTable(self, products):
        self.listProducts.tblProducts.setRowCount(len(products))
        for row, product in enumerate(products):
            self.listProducts.tblProducts.setItem(row, 0, QTableWidgetItem(str(product.name)))
            self.listProducts.tblProducts.setItem(row, 1, QTableWidgetItem(str(product.description)))
            self.listProducts.tblProducts.setItem(row, 2, QTableWidgetItem(str(product.category)))
            self.listProducts.tblProducts.setItem(row, 3, QTableWidgetItem(str(product.price)))
            self.listProducts.tblProducts.setItem(row, 4, QTableWidgetItem(product.isImported and "Si" or "No"))
            self.listProducts.tblProducts.setItem(row, 5, QTableWidgetItem(str(product.quantity)))

    def filterTable(self, text):
        for row in range(self.listProducts.tblProducts.rowCount()):
            match = False
            for column in range(self.listProducts.tblProducts.columnCount()):
                item = self.listProducts.tblProducts.item(row, column)
                if text.lower() in item.text().lower():
                    match = True
                    break
            self.listProducts.tblProducts.setRowHidden(row, not match)

    def openDetailProduct(self, row, column):
    # Obtenemos el producto seleccionado usando el índice de la fila
        product = self.products[row]
        self.detailProduct = ViewProduct(product)
