
from model.product import Product
import api.connectionRepository as con

class ProductRepository:
    def save(self, product: Product) -> bool:
        db = con.ConnectionRepository().connexionDatabase()
        try:
            cursor = db.cursor()
            query = """
                INSERT INTO products (name, description, category, price, isImported, quantity) 
                VALUES (?, ?, ?, ?, ?, ?);
            """
            cursor.execute(query, (
                product.name, product.description, product.category, product.price, 
                product.isImported, product.quantity
            ))
            db.commit()
            return True  # Guardado exitoso
        except Exception as e:
            print("Error al guardar el producto:", e)
            return False  # Ocurrió un error
        finally:
            db.close()

    def getAll(self) -> list[Product]:
        db = con.ConnectionRepository().connexionDatabase()
        try:
            cursor = db.cursor()
            query = """
                SELECT id, name, description, category, price, isImported, quantity 
                FROM products;
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            products = []
            for row in rows:
                product = Product(row[1], row[2], row[3], row[4], row[5], row[0], row[6]) 
                products.append(product)
            return products
        except Exception as e:
            print("Error al obtener los productos:", e)
            return [] 
        finally:
            db.close()

    def update(self, product: Product) -> bool:
        db = con.ConnectionRepository().connexionDatabase()
        try:
            cursor = db.cursor()
            query = """
                UPDATE products
                SET name = ?, description = ?, category = ?, price = ?, isImported = ?, quantity = ?
                WHERE id = ?;
            """
            cursor.execute(query, (
                product.name, product.description, product.category, 
                product.price, product.isImported, product.quantity, product.id
            ))
            db.commit()
            return True
        except Exception as e:
            print("Error al actualizar el producto:", e)
            return False
        finally:
            db.close()