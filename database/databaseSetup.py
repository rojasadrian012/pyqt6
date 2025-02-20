import sqlite3
import random
class DatabaseSetup:

    @staticmethod
    def connection():
        return sqlite3.connect("database/database.db") 
    
    @staticmethod
    def createTables():
        db = DatabaseSetup.connection()
        cursor = db.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                user TEXT UNIQUE,
                password TEXT
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                category TEXT,
                price INTEGER,
                isImported BOOLEAN,
                quantity INTEGER
            );
        """)

        db.commit()
        db.close()
        print("Tablas creadas correctamente.")

        DatabaseSetup.createUserAdmin()
        DatabaseSetup.insertSampleProducts()

    @staticmethod
    def verifyAndSetup():
        db = DatabaseSetup.connection()
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        table_exists = cursor.fetchone()  # 🔹 Retorna None si la tabla no existe

        db.close()

        if table_exists is None:
            print("⚠️ La base de datos está vacía. Creando estructura...")
            DatabaseSetup.createTables()
        else:
            print("✅ Las tablas 'users' y 'products' existen en la base de datos.")

    @staticmethod
    def createUserAdmin():
        try:
            db = DatabaseSetup.connection()
            db.cursor().execute(""" 
                INSERT OR IGNORE INTO users (name, user, password) 
                VALUES ('Admin', 'admin', 'admin');
            """)  
            db.commit()
            db.close()
        except Exception as e:
            print("Error al crear el usuario admin:", e)

    @staticmethod
    def insertSampleProducts():
        productos = [
            ("Laptop", "Laptop de alto rendimiento con 16GB RAM", "Electrónicos"),
            ("Celular", "Smartphone con pantalla OLED", "Electrónicos"),
            ("Auriculares", "Auriculares Bluetooth con cancelación de ruido", "Electrónicos"),
            ("Teclado mecánico", "Teclado gamer RGB con switches azules", "Electrónicos"),
            ("Monitor", "Monitor 27'' con resolución 4K", "Electrónicos"),
            ("Camisa", "Camisa formal de algodón", "Ropa"),
            ("Jeans", "Pantalón de mezclilla azul", "Ropa"),
            ("Zapatillas", "Zapatillas deportivas para correr", "Ropa"),
            ("Chaqueta", "Chaqueta de cuero negra", "Ropa"),
            ("Reloj", "Reloj de pulsera con correa de cuero", "Ropa"),
            ("Pan", "Pan artesanal con masa madre", "Alimentos"),
            ("Leche", "Leche descremada en envase de 1L", "Alimentos"),
            ("Queso", "Queso gouda en rodajas", "Alimentos"),
            ("Manzanas", "Manzanas rojas frescas", "Alimentos"),
            ("Chocolate", "Tableta de chocolate amargo 70%", "Alimentos"),
            ("Tablet", "Tablet con pantalla AMOLED de 10 pulgadas", "Electrónicos"),
            ("Smartwatch", "Reloj inteligente con monitor de frecuencia cardíaca", "Electrónicos"),
            ("Cámara", "Cámara fotográfica profesional con lente 50mm", "Electrónicos"),
            ("Router WiFi", "Router de alta velocidad con WiFi 6", "Electrónicos"),
            ("Impresora", "Impresora multifuncional a color", "Electrónicos"),
            ("Consola de videojuegos", "Consola de última generación con 2 controles", "Electrónicos"),
            ("Disco SSD", "Disco de estado sólido de 1TB", "Electrónicos"),
            ("Mouse inalámbrico", "Mouse ergonómico con sensor óptico", "Electrónicos"),
            ("Altavoz Bluetooth", "Altavoz portátil con sonido envolvente", "Electrónicos"),
            ("Cargador portátil", "Power bank de 20,000mAh", "Electrónicos"),
            ("Sudadera", "Sudadera con capucha de algodón", "Ropa"),
            ("Bufanda", "Bufanda de lana gruesa para invierno", "Ropa"),
            ("Pantalón de vestir", "Pantalón elegante para oficina", "Ropa"),
            ("Gorra", "Gorra de béisbol ajustable", "Ropa"),
            ("Vestido", "Vestido casual para verano", "Ropa"),
            ("Calcetines", "Pack de 5 pares de calcetines térmicos", "Ropa"),
            ("Shorts deportivos", "Shorts ligeros para correr", "Ropa"),
            ("Chaleco", "Chaleco acolchonado para invierno", "Ropa"),
            ("Botas", "Botas de cuero resistentes al agua", "Ropa"),
            ("Guantes", "Guantes táctiles para uso con smartphones", "Ropa"),
            ("Cereal", "Cereal integral sin azúcar", "Alimentos"),
            ("Jugo de naranja", "Jugo de naranja 100% natural", "Alimentos"),
            ("Café", "Café en grano de origen colombiano", "Alimentos"),
            ("Té verde", "Té verde en sobres con antioxidantes", "Alimentos"),
            ("Miel", "Miel pura de abeja en frasco de 500ml", "Alimentos"),
            ("Yogur", "Yogur natural sin azúcar añadido", "Alimentos"),
            ("Frijoles", "Frijoles negros enlatados", "Alimentos"),
            ("Arroz", "Arroz blanco de grano largo", "Alimentos"),
            ("Aceite de oliva", "Aceite de oliva extra virgen", "Alimentos"),
            ("Galletas", "Galletas integrales con chispas de chocolate", "Alimentos"),
            ("Helado", "Helado de vainilla sin conservantes", "Alimentos"),
            ("Salsa de tomate", "Salsa de tomate orgánica", "Alimentos"),
            ("Pasta", "Pasta italiana de trigo duro", "Alimentos"),
            ("Atún en lata", "Atún en agua con bajo contenido de sodio", "Alimentos"),
            ("Nueces", "Mix de nueces y frutos secos", "Alimentos")
        ]

        db = DatabaseSetup.connection()
        cursor = db.cursor()
                
        sql_insert_product = """
            INSERT INTO products (name, description, category, price, isImported, quantity)
            VALUES (?, ?, ?, ?, ?, ?);
        """

        for _ in range(50):
            name, descripcion, categoria = random.choice(productos)
            price = random.randint(10, 500) 
            isImported = random.choice([0, 1]) 
            quantity = random.randint(1, 100) 
            cursor.execute(sql_insert_product, (name, descripcion, categoria, price, isImported, quantity))
          
        db.commit()
        db.close()
        print("Se insertaron 50 productos aleatorios.")
