from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QTableWidgetItem

from api.productRepository import ProductRepository
from ui.main.components.newProduct.newProduct import NewProduct

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main/main.ui", self)
        self.products = []  # Guardamos la lista completa de productos
        self.initUi()
        self.showMaximized()
        self.updateTable()
        self.btnUpdateTable.clicked.connect(self.updateTable)
        self.tblProducts.setSortingEnabled(True)  # Habilitamos ordenamiento
        self.tblProducts.cellDoubleClicked.connect(self.openDetailProduct)  # Abrir detalle al hacer doble clic


    def initUi(self):
        self.btnNewProduct.triggered.connect(self.openNewProduct)
        self.qleSearch.textChanged.connect(self.filterTable)  # Conexión para el filtrado

    def openNewProduct(self):
        self.newProduct = NewProduct()

    def updateTable(self):
        self.products = ProductRepository().getAll()  # Obtenemos la lista completa
        self.populateTable(self.products)

    def populateTable(self, products):
        self.tblProducts.setRowCount(len(products))
        for row, product in enumerate(products):
            self.tblProducts.setItem(row, 0, QTableWidgetItem(str(product.name)))
            self.tblProducts.setItem(row, 1, QTableWidgetItem(str(product.description)))
            self.tblProducts.setItem(row, 2, QTableWidgetItem(str(product.category)))
            self.tblProducts.setItem(row, 3, QTableWidgetItem(str(product.price)))
            self.tblProducts.setItem(row, 4, QTableWidgetItem(str(product.isImported)))

    def filterTable(self, text):
        # Muestra solo las filas que contienen el texto en alguna de sus celdas
        for row in range(self.tblProducts.rowCount()):
            match = False
            for column in range(self.tblProducts.columnCount()):
                item = self.tblProducts.item(row, column)
                if text.lower() in item.text().lower():
                    match = True
                    break
            self.tblProducts.setRowHidden(row, not match)

    def openDetailProduct(self, row, column):
    # Obtenemos el producto seleccionado usando el índice de la fila
        product = self.products[row]
        self.detailProduct = NewProduct(product)