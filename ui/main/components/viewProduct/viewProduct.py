from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

from model.product import Product as ProductModel
from api.productRepository import ProductRepository

class ViewProduct:
    def __init__(self, product=None):
        self.product = product
        
        self.viewProduct = uic.loadUi("ui/main/components/viewProduct/viewProduct.ui")
        self.initUi()
        
        if self.product:
            self.loadProductData()
            self.viewProduct.lblProductViewTitle.setText("Editar Producto")
            self.viewProduct.lblProductViewTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.viewProduct.lblProductViewTitle.setStyleSheet("""
                font-family: 'Segoe UI';
                font-size: 18pt;
                font-weight: 700;
                color: #000000;
            """)
            
        self.viewProduct.show()
    
    def initUi(self):
        if self.product:
            self.viewProduct.btnSaveProduct.setText("Actualizar")
            self.viewProduct.btnSaveProduct.clicked.connect(self.updateProduct)
        else:
            self.viewProduct.btnSaveProduct.clicked.connect(self.saveProduct)
    
    def loadProductData(self):
        self.viewProduct.txtProductoName.setText(self.product.name)
        self.viewProduct.txtProductDescription.setText(self.product.description)
        self.viewProduct.cbxProductCategory.setCurrentText(self.product.category)
        self.viewProduct.txtProductoPrice.setText(str(self.product.price))
        self.viewProduct.chkIsImported.setChecked(self.product.isImported)
        self.viewProduct.txtProductQuantity.setText(str(self.product.quantity))
    
    def saveProduct(self):
        name = self.viewProduct.txtProductoName.text()
        description = self.viewProduct.txtProductDescription.text()
        category = self.viewProduct.cbxProductCategory.currentText()
        price = self.viewProduct.txtProductoPrice.text()
        quantity = self.viewProduct.txtProductQuantity.text()

        if not self.validateFields(name, description, category, price, quantity):
            print("ifff")
            return 

        self.product = ProductModel(
            None,  
            name,
            description,
            category,
            int(price),
            self.viewProduct.chkIsImported.isChecked(),
            int(quantity)
        )

        productApi = ProductRepository()
        if productApi.save(self.product):
            QMessageBox.information(
                self.viewProduct,
                "Producto Guardado",
                "El producto se ha guardado correctamente.",
                QMessageBox.StandardButton.Ok
            )
            self.viewProduct.hide()
        else:
            QMessageBox.critical(
                self.viewProduct,
                "Error",
                "Hubo un problema al guardar el producto.",
                QMessageBox.StandardButton.Ok
            )
    def updateProduct(self):
        name = self.viewProduct.txtProductoName.text()
        description = self.viewProduct.txtProductDescription.text()
        category = self.viewProduct.cbxProductCategory.currentText()
        price = self.viewProduct.txtProductoPrice.text()
        quantity = self.viewProduct.txtProductQuantity.text()

        if not self.validateFields(name, description, category, price, quantity):
            return 

        self.product.name = name
        self.product.description = description
        self.product.category = category
        self.product.price = int(price)
        self.product.isImported = self.viewProduct.chkIsImported.isChecked()
        self.product.quantity = quantity

        productApi = ProductRepository()
        if productApi.update(self.product):
            QMessageBox.information(
                self.viewProduct,
                "Producto Actualizado",
                "El producto se ha actualizado correctamente.",
                QMessageBox.StandardButton.Ok
            )
            self.viewProduct.hide()
        else:
            QMessageBox.critical(
                self.viewProduct,
                "Error",
                "Hubo un problema al actualizar el producto.",
                QMessageBox.StandardButton.Ok
            )
    def validateFields(self, name, description, category, price, quantity):
        color = "color: red;"
        self.viewProduct.errProductoName.setStyleSheet(color)
        self.viewProduct.errProductoName.setText("")
        self.viewProduct.errProductDescription.setStyleSheet(color)
        self.viewProduct.errProductDescription.setText("")
        self.viewProduct.errProductCategory.setStyleSheet(color)
        self.viewProduct.errProductCategory.setText("")
        self.viewProduct.errProductoPrice.setStyleSheet(color)
        self.viewProduct.errProductoPrice.setText("")
        self.viewProduct.errProductQuantity.setStyleSheet(color)
        self.viewProduct.errProductQuantity.setText("")

        errors = False

        if len(name) < 2:
            self.viewProduct.errProductoName.setText("Escriba un nombre válido.")
            self.viewProduct.txtProductoName.setFocus()
            errors = True
        if len(description) < 2:
            self.viewProduct.errProductDescription.setText("Escriba una descripción válida.")
            errors = True
        if category == "--- Selecione una opcción":
            self.viewProduct.errProductCategory.setText("Seleccione una categoría.")
            errors = True
        if not price.isnumeric():
            self.viewProduct.errProductoPrice.setText("El precio debe ser un número.")
            self.viewProduct.txtProductoPrice.setText("0")
            errors = True
        elif int(price) < 1:
            self.viewProduct.errProductoPrice.setText("El precio debe ser mayor a cero.")
            errors = True
        if not quantity.isnumeric():
            self.viewProduct.errProductQuantity.setText("La cantidad debe ser un número.")
            self.viewProduct.txtProductQuantity.setText("0")
            errors = True
        elif int(quantity) < 1:
            self.viewProduct.errProductQuantity.setText("La cantidad debe ser mayor a cero.")
            errors = True

        return not errors 
