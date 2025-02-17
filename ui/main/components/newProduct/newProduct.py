from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

from model.product import Product as ProductModel
from api.productRepository import ProductRepository

class NewProduct:
    def __init__(self, product=None):
        # Si se pasa un producto, se entra en modo edición (detalle)
        self.product = product
        
        # Carga la interfaz de usuario
        self.vNewProduct = uic.loadUi("ui/main/components/newProduct/newProduct.ui")
        self.initUi()
        
        # Si hay un producto, cargar sus datos en la interfaz
        if self.product:
            self.loadProductData()
            self.vNewProduct.lblProductViewTitle.setText("Editar Producto")
            self.vNewProduct.lblProductViewTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.vNewProduct.lblProductViewTitle.setStyleSheet("""
                font-family: 'Segoe UI';
                font-size: 18pt;
                font-weight: 700;
                color: #000000;
            """)
            
        self.vNewProduct.show()
    
    def initUi(self):
        if self.product:
            # Modo edición: cambiar texto del botón y conectar a la función de actualización
            self.vNewProduct.btnSaveProduct.setText("Actualizar")
            self.vNewProduct.btnSaveProduct.clicked.connect(self.updateProduct)
        else:
            # Modo creación: se conecta la función para guardar un nuevo producto
            self.vNewProduct.btnSaveProduct.clicked.connect(self.saveProduct)
    
    def loadProductData(self):
        """Carga los datos del producto en los campos de la interfaz."""
        self.vNewProduct.txtProductoName.setText(self.product.name)
        # Se corrige el nombre del widget de descripción:
        self.vNewProduct.txtProductDescription.setText(self.product.description)
        self.vNewProduct.cbxProductCategory.setCurrentText(self.product.category)
        self.vNewProduct.txtProductoPrice.setText(str(self.product.price))
        self.vNewProduct.chkIsImported.setChecked(self.product.isImported)
    
    def saveProduct(self):
        """Guarda un nuevo producto en la base de datos."""
        name = self.vNewProduct.txtProductoName.text()
        # Se corrige el nombre del widget de descripción:
        description = self.vNewProduct.txtProductDescription.text()
        category = self.vNewProduct.cbxProductCategory.currentText()
        price = self.vNewProduct.txtProductoPrice.text()

        color = "color: red;"

        # Reiniciar mensajes de error
        self.vNewProduct.errProductoName.setStyleSheet(color)
        self.vNewProduct.errProductoName.setText("")
        self.vNewProduct.errProductDescription.setStyleSheet(color)
        self.vNewProduct.errProductDescription.setText("")
        self.vNewProduct.errProductCategory.setStyleSheet(color)
        self.vNewProduct.errProductCategory.setText("")
        self.vNewProduct.errProductoPrice.setStyleSheet(color)
        self.vNewProduct.errProductoPrice.setText("")

        # Validaciones
        if len(name) < 2:
            self.vNewProduct.errProductoName.setText("Escriba un nombre válido.")
            self.vNewProduct.txtProductoName.setFocus()
        elif len(description) < 2:
            self.vNewProduct.errProductDescription.setText("Escriba una descripción válida.")
            self.vNewProduct.txtProductDescription.setFocus()
        elif category == "--- Selecione una opcción":
            self.vNewProduct.errProductCategory.setText("Seleccione una categoría.")
            self.vNewProduct.cbxProductCategory.setFocus()
        elif not price.isnumeric():
            self.vNewProduct.errProductoPrice.setText("El precio debe ser un número.")
            self.vNewProduct.txtProductoPrice.setText("0")
            self.vNewProduct.txtProductoPrice.setFocus()
        elif int(price) < 1:
            self.vNewProduct.errProductoPrice.setText("El precio debe ser mayor a cero.")
            self.vNewProduct.txtProductoPrice.setFocus()
        else:
            # Crear el objeto producto nuevo
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

    def updateProduct(self):
        """Actualiza los datos de un producto existente."""
        name = self.vNewProduct.txtProductoName.text()
        # Se corrige el nombre del widget de descripción:
        description = self.vNewProduct.txtProductDescription.text()
        category = self.vNewProduct.cbxProductCategory.currentText()
        price = self.vNewProduct.txtProductoPrice.text()

        color = "color: red;"

        # Reiniciar mensajes de error
        self.vNewProduct.errProductoName.setStyleSheet(color)
        self.vNewProduct.errProductoName.setText("")
        self.vNewProduct.errProductDescription.setStyleSheet(color)
        self.vNewProduct.errProductDescription.setText("")
        self.vNewProduct.errProductCategory.setStyleSheet(color)
        self.vNewProduct.errProductCategory.setText("")
        self.vNewProduct.errProductoPrice.setStyleSheet(color)
        self.vNewProduct.errProductoPrice.setText("")

        # Validaciones (similares a las de guardado)
        if len(name) < 2:
            self.vNewProduct.errProductoName.setText("Escriba un nombre válido.")
            self.vNewProduct.txtProductoName.setFocus()
        elif len(description) < 2:
            self.vNewProduct.errProductDescription.setText("Escriba una descripción válida.")
            self.vNewProduct.txtProductDescription.setFocus()
        elif category == "--- Selecione una opcción":
            self.vNewProduct.errProductCategory.setText("Seleccione una categoría.")
            self.vNewProduct.cbxProductCategory.setFocus()
        elif not price.isnumeric():
            self.vNewProduct.errProductoPrice.setText("El precio debe ser un número.")
            self.vNewProduct.txtProductoPrice.setText("0")
            self.vNewProduct.txtProductoPrice.setFocus()
        elif int(price) < 1:
            self.vNewProduct.errProductoPrice.setText("El precio debe ser mayor a cero.")
            self.vNewProduct.txtProductoPrice.setFocus()
        else:
            # Actualizar el objeto producto con los nuevos datos
            self.product.name = name
            self.product.description = description
            self.product.category = category
            self.product.price = int(price)
            self.product.isImported = self.vNewProduct.chkIsImported.isChecked()

            productApi = ProductRepository()
            if productApi.update(self.product):
                QMessageBox.information(
                    self.vNewProduct,
                    "Producto Actualizado",
                    "El producto se ha actualizado correctamente.",
                    QMessageBox.StandardButton.Ok
                )
            else:
                QMessageBox.critical(
                    self.vNewProduct,
                    "Error",
                    "Hubo un problema al actualizar el producto.",
                    QMessageBox.StandardButton.Ok
                )
            self.vNewProduct.hide()
