from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

from model.product import Product as ProductModel
from api.productRepository import ProductRepository

class ViewProduct:
    def __init__(self, product=None):
        # Si se pasa un producto, se entra en modo edición (detalle)
        self.product = product
        
        # Carga la interfaz de usuario
        self.viewProduct = uic.loadUi("ui/main/components/viewProduct/viewProduct.ui")
        self.initUi()
        
        # Si hay un producto, cargar sus datos en la interfaz
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
            # Modo edición: cambiar texto del botón y conectar a la función de actualización
            self.viewProduct.btnSaveProduct.setText("Actualizar")
            self.viewProduct.btnSaveProduct.clicked.connect(self.updateProduct)
        else:
            # Modo creación: se conecta la función para guardar un nuevo producto
            self.viewProduct.btnSaveProduct.clicked.connect(self.saveProduct)
    
    def loadProductData(self):
        """Carga los datos del producto en los campos de la interfaz."""
        self.viewProduct.txtProductoName.setText(self.product.name)
        # Se corrige el nombre del widget de descripción:
        self.viewProduct.txtProductDescription.setText(self.product.description)
        self.viewProduct.cbxProductCategory.setCurrentText(self.product.category)
        self.viewProduct.txtProductoPrice.setText(str(self.product.price))
        self.viewProduct.chkIsImported.setChecked(self.product.isImported)
    
    def saveProduct(self):
        """Guarda un nuevo producto en la base de datos."""
        name = self.viewProduct.txtProductoName.text()
        # Se corrige el nombre del widget de descripción:
        description = self.viewProduct.txtProductDescription.text()
        category = self.viewProduct.cbxProductCategory.currentText()
        price = self.viewProduct.txtProductoPrice.text()

        color = "color: red;"

        # Reiniciar mensajes de error
        self.viewProduct.errProductoName.setStyleSheet(color)
        self.viewProduct.errProductoName.setText("")
        self.viewProduct.errProductDescription.setStyleSheet(color)
        self.viewProduct.errProductDescription.setText("")
        self.viewProduct.errProductCategory.setStyleSheet(color)
        self.viewProduct.errProductCategory.setText("")
        self.viewProduct.errProductoPrice.setStyleSheet(color)
        self.viewProduct.errProductoPrice.setText("")

        # Validaciones
        if len(name) < 2:
            self.viewProduct.errProductoName.setText("Escriba un nombre válido.")
            self.viewProduct.txtProductoName.setFocus()
        elif len(description) < 2:
            self.viewProduct.errProductDescription.setText("Escriba una descripción válida.")
            self.viewProduct.txtProductDescription.setFocus()
        elif category == "--- Selecione una opcción":
            self.viewProduct.errProductCategory.setText("Seleccione una categoría.")
            self.viewProduct.cbxProductCategory.setFocus()
        elif not price.isnumeric():
            self.viewProduct.errProductoPrice.setText("El precio debe ser un número.")
            self.viewProduct.txtProductoPrice.setText("0")
            self.viewProduct.txtProductoPrice.setFocus()
        elif int(price) < 1:
            self.viewProduct.errProductoPrice.setText("El precio debe ser mayor a cero.")
            self.viewProduct.txtProductoPrice.setFocus()
        else:
            # Crear el objeto producto nuevo
            product = ProductModel(
                name,
                description,
                category,
                int(price),
                self.viewProduct.chkIsImported.isChecked()
            )
            productApi = ProductRepository()
            if productApi.save(product):
                QMessageBox.information(
                    self.viewProduct,
                    "Producto Guardado",
                    "El producto se ha guardado correctamente.",
                    QMessageBox.StandardButton.Ok
                )
            else:
                QMessageBox.critical(
                    self.viewProduct,
                    "Error",
                    "Hubo un problema al guardar el producto.",
                    QMessageBox.StandardButton.Ok
                )
            self.viewProduct.hide()

    def updateProduct(self):
        """Actualiza los datos de un producto existente."""
        name = self.viewProduct.txtProductoName.text()
        # Se corrige el nombre del widget de descripción:
        description = self.viewProduct.txtProductDescription.text()
        category = self.viewProduct.cbxProductCategory.currentText()
        price = self.viewProduct.txtProductoPrice.text()

        color = "color: red;"

        # Reiniciar mensajes de error
        self.viewProduct.errProductoName.setStyleSheet(color)
        self.viewProduct.errProductoName.setText("")
        self.viewProduct.errProductDescription.setStyleSheet(color)
        self.viewProduct.errProductDescription.setText("")
        self.viewProduct.errProductCategory.setStyleSheet(color)
        self.viewProduct.errProductCategory.setText("")
        self.viewProduct.errProductoPrice.setStyleSheet(color)
        self.viewProduct.errProductoPrice.setText("")

        # Validaciones (similares a las de guardado)
        if len(name) < 2:
            self.viewProduct.errProductoName.setText("Escriba un nombre válido.")
            self.viewProduct.txtProductoName.setFocus()
        elif len(description) < 2:
            self.viewProduct.errProductDescription.setText("Escriba una descripción válida.")
            self.viewProduct.txtProductDescription.setFocus()
        elif category == "--- Selecione una opcción":
            self.viewProduct.errProductCategory.setText("Seleccione una categoría.")
            self.viewProduct.cbxProductCategory.setFocus()
        elif not price.isnumeric():
            self.viewProduct.errProductoPrice.setText("El precio debe ser un número.")
            self.viewProduct.txtProductoPrice.setText("0")
            self.viewProduct.txtProductoPrice.setFocus()
        elif int(price) < 1:
            self.viewProduct.errProductoPrice.setText("El precio debe ser mayor a cero.")
            self.viewProduct.txtProductoPrice.setFocus()
        else:
            # Actualizar el objeto producto con los nuevos datos
            self.product.name = name
            self.product.description = description
            self.product.category = category
            self.product.price = int(price)
            self.product.isImported = self.viewProduct.chkIsImported.isChecked()

            productApi = ProductRepository()
            if productApi.update(self.product):
                QMessageBox.information(
                    self.viewProduct,
                    "Producto Actualizado",
                    "El producto se ha actualizado correctamente.",
                    QMessageBox.StandardButton.Ok
                )
            else:
                QMessageBox.critical(
                    self.viewProduct,
                    "Error",
                    "Hubo un problema al actualizar el producto.",
                    QMessageBox.StandardButton.Ok
                )
            self.viewProduct.hide()
