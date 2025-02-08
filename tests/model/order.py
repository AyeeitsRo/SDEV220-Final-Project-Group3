
SALES_TAX = 1.07

class FoodItem:
    def __init__(self, name: str, price: float, photo = None):
        self.name = name
        self.price = price
        self.photo = photo
        self.quantity: int = 1
    
    def __str__(self) -> str:
        return f'Food: {self.name}, Price: {self.price:.2f}, QTY: {self.quantity}'


class DrinkItem:
    def __init__(self, name: str, price: float, photo = None):
        self.name = name
        self.price = price
        self.photo = photo
        self.quantity: int = 1
    
    def __str__(self) -> str:
        return f'Drink: {self.name}, Price: {self.price:.2f}, QTY: {self.quantity}'


class Order:
    def __init__(self):
        self.items: list = [] # Holds list of user order
        self.total: float = 0.0 

    @property
    def add_total(self) -> float:
        """Calculates the total price of user order"""
        total = 0.0
        for item in self.items:
            total += item.price * item.quantity
        taxed_total: float = total * SALES_TAX
        return f"{taxed_total:.2f}"
    
    def add_item(self, item, quantity) -> None:
        """Add an item to user order"""
        item.quantity = quantity
        self.items.append(item)
        self.total = self.add_total
        
    def remove_item(self, item) -> None:
        """Remove an item from user order"""
        self.items.remove(item)
        self.total = self.add_total
        
    def clear_order(self) -> None:
        """Clears all items from user order"""
        self.items = []
        self.total = 0.0
    
    def __str__(self) -> str:
        """Returns str of items"""
        item_details = "\n".join(str(item) for item in self.items)
        return f'Items in order: \n{item_details}\n\nTotal: {self.total}'


# Drinks the cafe sells
BLACK_COFFEE = DrinkItem('Black Coffee', 3.00, 'resources/images/black_coffee.png') 
LATTE = DrinkItem('Latte', 8.50, 'resources/images/latte.png')
CAPPUCCINO = DrinkItem('Capppuccino', 7.00, 'resources/images/cappuccino.png')
ORANGE_JUICE = DrinkItem('Orange Juice', 5.50, 'resources/images/orange_juice.png')

# Food the cafe sells
CAKE_POP = FoodItem('Cake Pop', 3.50, 'resources/images/cake_pop.png')
CROISSANT = FoodItem('Croissant', 7.25, 'resources/images/croissant.png')
COFFEE_CAKE = FoodItem('Cinnamon Coffee Cake', 6.75, 'resources/images/coffee_cake.png')
CHOC_CHIP_COOKIE = FoodItem('Chocolate Chip Cookie', 3.00, 'resources/images/choc_chip_cookie.png')


order = Order()

"""
Example below of order output along with total
**RUN CODE TO SEE OUTPUT**
"""
order.add_item(LATTE, quantity=1)
order.add_item(CAPPUCCINO, quantity = 2)
order.add_item(CAKE_POP, quantity = 3)
order.add_item(COFFEE_CAKE, quantity = 2)

print(order)