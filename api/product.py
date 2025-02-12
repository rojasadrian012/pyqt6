
from model.product import Product
import data.connection as con

class Product:
    def save(self, product: "Product") -> bool:
        db = con.Connection().connectDatabase()
        try:
            cursor = db.cursor()
            query = """
                INSERT INTO products (name, description, category, price, isImported) 
                VALUES (?, ?, ?, ?, ?);
            """
            cursor.execute(query, (product.name, product.description, product.category, product.price, product.isImported))
            db.commit()
            return True  # Guardado exitoso
        except Exception as e:
            print("Error al guardar el producto:", e)
            return False  # Ocurrió un error
        finally:
            db.close()
