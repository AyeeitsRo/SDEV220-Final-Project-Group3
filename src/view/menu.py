"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QListWidget
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cafe Menu")
        self.setGeometry(100, 100, 900, 650)
        
        menu_layout = QVBoxLayout()

        # Horizontal layout for the header of the menu and close button
        top_container = QHBoxLayout()
        # Header Label
        header_label = QLabel("Cafe Menu")
        
        # Close Button
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        # Add widgets to top_container
        top_container.addWidget(header_label, 3)
        top_container.addWidget(close_button, 1)
        
        # Add the top layout to the main layout
        menu_layout.addLayout(top_container) # Keep this in the first position to keep it at the top.
        
        self.setLayout(menu_layout)
        
        self.right_container = QWidget()
        right_side = QVBoxLayout(self.right_container)
        self.right_container.setStyleSheet("background-color: #201212; border: 3px solid #8b0000; border-radius: 10px; padding: 5px;")
        self.right_label = QLabel("Some words here")
        self.right_label.setFont(QFont("Arial", 16, QFont.Weight.Light))
        self.right_label.setStyleSheet("background-color: transparent; border: none;")
        self.right_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_highlight = QListWidget()   
        
        right_side.addWidget(self.right_label)
        right_side.addWidget(self.profile_highlight) 

"""





from model.order import *
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea

class DrinkItem:
    def __init__(self, name, price, image_path):
        self.name = name
        self.price = price
        self.image_path = image_path

class FoodItem:
    def __init__(self, name, price, image_path):
        self.name = name
        self.price = price
        self.image_path = image_path

class MenuWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Cafe Menu")
        self.setGeometry(100, 100, 900, 650)
        self.setStyleSheet("background-color: black;")

        # Create the layout for the window
        menu_layout = QVBoxLayout()

        # Top Header
        header_label = QLabel("CAFE ORDER")
        header_label.setStyleSheet("color: white; font-size: 24px; border: 2px solid red; border-radius: 10px; padding: 10px;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        menu_layout.addWidget(header_label)


        # Create a horizontal layout to separate left and right sections
        menu_h_layout = QHBoxLayout()
        
        # Left side (Drink and Food Items)
        left_frame = QFrame()
        left_frame.setStyleSheet("background-color: black; border-radius: 10px;")
        left_layout = QVBoxLayout(left_frame)

        # Drinks section
        drink_section = QLabel("Drinks")
        drink_section.setStyleSheet("color: white; font-size: 18px;")
        left_layout.addWidget(drink_section)

        # Add drinks to the layout
        drinks = [BLACK_COFFEE, LATTE, CAPPUCCINO, ORANGE_JUICE]
        
        for drink in drinks:
            drink_item_frame = self.create_item_frame(drink.name, drink.price, drink.photo)
            left_layout.addWidget(drink_item_frame)

        # Food section
        food_section = QLabel("Food")
        food_section.setStyleSheet("color: white; font-size: 18px;")
        left_layout.addWidget(food_section)

        # Add food to the layout
        foods = [CAKE_POP, CROISSANT, COFFEE_CAKE, CHOC_CHIP_COOKIE]
        
        for food in foods:
            food_item_frame = self.create_item_frame(food.name, food.price, food.photo)
            left_layout.addWidget(food_item_frame)
        
        # Right side (Cart Area) - Adding a red border here
        right_frame = QFrame()
        right_frame.setStyleSheet("background-color: black; border: 2px solid red; border-radius: 10px;")  # Red border added for cart
        right_layout = QVBoxLayout(right_frame)

        # Cart section
        cart_label = QLabel("Cart")
        cart_label.setStyleSheet("color: white; font-size: 18px;")
        right_layout.addWidget(cart_label)
        right_layout.addWidget(right_frame)
        
        # Left Scroll area
        l_scroll_area = QScrollArea()
        l_scroll_area.setWidgetResizable(True)
        l_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Show vertical scroll
        l_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Hide horizontal scroll
        l_scroll_area.setWidget(left_frame)
        
        # Right Scroll area
        r_scroll_area = QScrollArea()
        r_scroll_area.setWidgetResizable(True)
        r_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Show vertical scroll
        r_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Hide horizontal scroll
        r_scroll_area.setWidget(right_frame)

        # Add the left and right frame to the horizontal layout
        menu_h_layout.addWidget(l_scroll_area, 2)  # 2: Take up more space
        menu_h_layout.addWidget(r_scroll_area, 1)  # 1: Take up less space


        # Add the horizontal layout to the main layout
        menu_layout.addLayout(menu_h_layout)

        # Set the layout for the window
        self.setLayout(menu_layout)

    def create_item_frame(self, item_name, item_price, image_path):
        # Frame to hold each item, with red border only on the item itself
        item_frame = QFrame()
        item_frame.setStyleSheet("border: 1px solid red; border-radius: 10px; background-color: black; padding: 5px;")
        item_layout = QHBoxLayout(item_frame)

        # Image
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(QSize(50, 50), Qt.AspectRatioMode.KeepAspectRatio)  # Resize image
        image_label.setPixmap(pixmap)
        
        # Item Name and Price
        item_info = QLabel(f"{item_name}\n${item_price:.2f}")
        item_info.setStyleSheet("color: white; font-size: 14px;")

        # Add to Cart button
        add_button = QPushButton("Add to Cart")
        add_button.setStyleSheet("background-color: red; color: white; border-radius: 5px; padding: 5px;")
        add_button.clicked.connect(lambda: self.controller.add_to_cart(item_name, item_price))

        # Add all widgets to the item frame layout
        item_layout.addWidget(image_label)
        item_layout.addWidget(item_info)
        item_layout.addWidget(add_button)

        return item_frame