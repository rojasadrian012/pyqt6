from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

from model.product import Product as ProductModel
from api.productRepository import ProductRepository

class NewProduct:
    def __init__(self):
        # Carga la interfaz de usuario
        self.vNewProduct = uic.loadUi("ui/main/components/newProduct/newProduct.ui")
        self.initUi()
        self.vNewProduct.show()
    
    def initUi(self):
        self.vNewProduct.btnSaveProduct.clicked.connect(self.saveProduct)
    
    def saveProduct(self):
        name = self.vNewProduct.txtProductoName.text()
        description = self.vNewProduct.txtProductDescription.text()
        category = self.vNewProduct.cbxProductCategory.currentText()
        price = self.vNewProduct.txtProductoPrice.text()

        color = "color: red;"

        self.vNewProduct.errProductoName.setStyleSheet(color)
        self.vNewProduct.errProductoName.setText("")
        self.vNewProduct.errProductDescription.setStyleSheet(color)
        self.vNewProduct.errProductDescription.setText("")
        self.vNewProduct.errProductCategory.setStyleSheet(color)
        self.vNewProduct.errProductCategory.setText("")
        self.vNewProduct.errProductoPrice.setStyleSheet(color)
        self.vNewProduct.errProductoPrice.setText("")

        if len(name) < 2:
            self.vNewProduct.errProductoName.setText("Escriba un nombre válido.")
            self.vNewProduct.txtProductoName.setFocus()
        elif len(description) < 2:
            self.vNewProduct.errProductDescription.setText("Escriba una descripcion válida.")
            self.vNewProduct.txtProductDescription.setFocus()
        elif category == "--- Selecione una opcción":
            self.vNewProduct.errProductCategory.setText("Seleccione una categoria.")
            self.vNewProduct.cbxProductCategory.setFocus()
        elif not price.isnumeric():
            self.vNewProduct.errProductoPrice.setText("El precio debe ser un número.")
            self.vNewProduct.txtProductoPrice.setText("0")
            self.vNewProduct.txtProductoPrice.setFocus()
        elif int(price) < 1:
            self.vNewProduct.errProductoPrice.setText("El precio debe ser mayor a cero.")
            self.vNewProduct.txtProductoPrice.setFocus()
        else:
            product = ProductModel(
                name,
                description,
                category,
                int(price),
                self.vNewProduct.chkIsImported.isChecked()
            )
            productApi = ProductRepository()
            if productApi.save(product):
                QMessageBox.information(
                    self.vNewProduct,
                    "Producto Guardado",
                    "El producto se ha guardado correctamente.",
                    QMessageBox.StandardButton.Ok
                )
            else:
                QMessageBox.critical(
                    self.vNewProduct,
                    "Error",
                    "Hubo un problema al guardar el producto.",
                    QMessageBox.StandardButton.Ok
                )

            self.vNewProduct.hide()

                
            self.vNewProduct.hide()
