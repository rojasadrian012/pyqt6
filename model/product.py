class Product:
    def __init__(self, name=str, description=str, category=str, price=int, isImported=bool, id=None):
        self.name = name    
        self.description = description
        self.category = category
        self.price = price
        self.isImported = isImported
        self.id = id  