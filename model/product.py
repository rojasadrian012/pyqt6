class Product:
    def __init__(self, id=None, name=str, description=str, category=str, price=int, isImported=bool, quantity=int):
        self.id = id  
        self.name = name    
        self.description = description
        self.category = category
        self.price = price
        self.isImported = isImported
        self.quantity = quantity