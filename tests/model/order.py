from abc import abstractmethod

class Order:
    def __init__(self, items, price, quantity, total, photo):
        self.items = {
            
        }
        self.price = price
        self.quantity = quantity
        self.total = total
        self.photo = photo
    
    @property
    @abstractmethod
    def add_total(self, price, total):
        """Property abstract method, will be implemented by child classes"""
        pass
    
    def add_cart(self):
        # Allow for adding multiple, deleting, then submit to back end
        pass
    
    def __str__(self):
        return f'Item: {self.item}, Price: {self.price}'
    

class FoodItem:
    pass


class DrinkItem:
    pass