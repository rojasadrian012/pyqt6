from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QTableWidgetItem
import pyqtgraph as pg
import numpy as np

from api.productRepository import ProductRepository
from ui.main.components.viewProduct.viewProduct import ViewProduct
from ui.main.components.listProducts.listProducts import ListProducts

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main/main.ui", self)
        self.products = [] 
        self.initUi()
        self.initGraphs()  
        self.showMaximized()
        self.getProducts()  

    def initUi(self):
        self.btnNewProduct.triggered.connect(self.openNewProduct)
        self.btnListProducts.triggered.connect(self.openListProduct)
        
    def getProducts(self):
        self.products = ProductRepository().getAll()  
        self.updateGraphs()    

    def initGraphs(self):
        # Creamos dos widgets de gráficos con fondo blanco
        self.graphWidget1 = pg.PlotWidget(background='w')
        self.graphWidget2 = pg.PlotWidget(background='w')
        
        # Agregamos los gráficos al layout del widget central
        layout = self.centralWidget().layout()
        if layout is not None:
            layout.addWidget(self.graphWidget1)
            layout.addWidget(self.graphWidget2)
        else:
            # Si no existe un layout, lo creamos
            new_layout = QVBoxLayout(self.centralWidget())
            new_layout.addWidget(self.tblProducts)
            new_layout.addWidget(self.graphWidget1)
            new_layout.addWidget(self.graphWidget2)

    def updateGraphs(self):
    # Limpiamos las gráficas anteriores
        self.graphWidget1.clear()
        self.graphWidget2.clear()

        # --- Gráfica 1: Relación entre Precio y Cantidad (Scatter Plot) ---
        if self.products:
            quantities = [product.quantity for product in self.products]
            prices = [product.price for product in self.products]
            
            # Scatter plot con símbolos
            self.graphWidget1.plot(
                x=quantities, 
                y=prices, 
                pen=None,  # Sin línea conectando puntos
                symbol='o', 
                symbolBrush=(85, 255, 127), 
                symbolSize=8
            )
            self.graphWidget1.setTitle("Relación entre Precio y Cantidad")
            self.graphWidget1.setLabel('left', "Precio")
            self.graphWidget1.setLabel('bottom', "Cantidad")

        # --- Gráfica 2: Cantidad total de productos por categoría ---
        categorias = {}
        for product in self.products:
            categoria = product.category
            # Sumamos la cantidad de cada producto a su categoría
            if categoria in categorias:
                categorias[categoria] += product.quantity
            else:
                categorias[categoria] = product.quantity

        if categorias:
            cats = list(categorias.keys())
            total_por_categoria = list(categorias.values())
            x = np.arange(len(cats))
            
            # Barras representando la cantidad total por categoría
            bg = pg.BarGraphItem(
                x=x, 
                height=total_por_categoria, 
                width=0.6, 
                brush=(85, 255, 127)
            )
            self.graphWidget2.addItem(bg)
            
            # Configurar ejes
            self.graphWidget2.getAxis('bottom').setTicks([list(zip(x, cats))])
            self.graphWidget2.setTitle("Cantidad de Productos por Categoría")
            self.graphWidget2.setLabel('left', "Cantidad Total")
            self.graphWidget2.setLabel('bottom', "Categoría")

    def openNewProduct(self):
        self.newProduct = ViewProduct(None)

    def openListProduct(self):
        self.listProduct = ListProducts()
