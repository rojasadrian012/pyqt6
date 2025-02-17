
from model.product import Product
import api.connectionRepository as con

class ProductRepository:
    def save(self, product: "ProductRepository") -> bool:
        db = con.ConnectionRepository().connectDatabase()
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

    def getAll(self) -> list[Product]:
        db = con.ConnectionRepository().connectDatabase()
        try:
            cursor = db.cursor()
            query = """
                SELECT id, name, description, category, price, isImported 
                FROM products;
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            products = []
            for row in rows:
                product = Product(row[1], row[2], row[3], row[4], row[5], row[0])  # Ahora incluye el id
                products.append(product)
            return products
        except Exception as e:
            print("Error al obtener los productos:", e)
            return [] 
        finally:
            db.close()

    def update(self, product: Product) -> bool:
        db = con.ConnectionRepository().connectDatabase()
        try:
            cursor = db.cursor()
            query = """
                UPDATE products
                SET name = ?, description = ?, category = ?, price = ?, isImported = ?
                WHERE id = ?;
            """
            cursor.execute(query, (product.name, product.description, product.category, product.price, product.isImported, product.id))
            db.commit()
            return True
        except Exception as e:
            print("Error al actualizar el producto:", e)
            return False
        finally:
            db.close()