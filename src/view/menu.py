
from view.cart_popup import *
from model.order import *      
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap

class MenuWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Cafe Menu")
        self.setGeometry(100, 100, 900, 700)
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
            drink_item_frame = self.create_item_frame(drink)
            left_layout.addWidget(drink_item_frame)

        # Food section
        food_section = QLabel("Food")
        food_section.setStyleSheet("color: white; font-size: 18px;")
        left_layout.addWidget(food_section)

        # Add food to the layout
        foods = [CAKE_POP, CROISSANT, COFFEE_CAKE, CHOC_CHIP_COOKIE]
        for food in foods:
            food_item_frame = self.create_item_frame(food)
            left_layout.addWidget(food_item_frame)

        # Right side (Cart Area)
        right_frame = QFrame()
        right_frame.setStyleSheet("background-color: black; border: 2px solid red; border-radius: 10px;")
        right_layout = QVBoxLayout(right_frame)
        right_frame.setMaximumWidth(300)

        # Cart section
        self.cart_display = QVBoxLayout()  
        right_layout.addLayout(self.cart_display)

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

        # Create the 'View Cart' button
        view_cart_button = QPushButton("View Cart")
        view_cart_button.setStyleSheet("background-color: red; color: white; border-radius: 5px; padding: 10px;")
        view_cart_button.clicked.connect(self.open_cart_popup)  # Open the cart popup when clicked

        menu_layout.addWidget(view_cart_button)

        # Set the layout for the window
        self.setLayout(menu_layout)

    def create_item_frame(self, item):
        # Frame to hold each item
        item_frame = QFrame()
        item_frame.setStyleSheet("border: 1px solid red; border-radius: 10px; background-color: black; padding: 5px;")
        item_layout = QHBoxLayout(item_frame)

        # Image
        image_label = QLabel()
        pixmap = QPixmap(item.photo)
        pixmap = pixmap.scaled(QSize(50, 50), Qt.AspectRatioMode.KeepAspectRatio)  # Resize image
        image_label.setPixmap(pixmap)

        # Item Name and Price
        item_info = QLabel(f"{item.name}\n${item.price:.2f}")
        item_info.setStyleSheet("color: white; font-size: 14px;")

        # Add to Cart button
        add_button = QPushButton("Add to Cart")
        add_button.setStyleSheet("background-color: red; color: white; border-radius: 5px; padding: 5px;")
        add_button.clicked.connect(lambda: self.controller.add_to_cart(item))  # Pass the item to add it to cart

        # Add all widgets to the item frame layout
        item_layout.addWidget(image_label)
        item_layout.addWidget(item_info)
        item_layout.addWidget(add_button)

        return item_frame

    def update_cart_ui(self):
        """Updates the cart display when an item is added to the cart."""
        # Clear the current cart display
        for i in reversed(range(self.cart_display.count())):
            widget = self.cart_display.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Add each item in the order to the cart display
        for item in order.items:
            # Create labels for the item name, quantity, and price
            item_label = QLabel(f"{item.name} - {item.quantity} x ${item.price:.2f}")
            item_label.setWordWrap(True)
            item_label.setStyleSheet("color: white; font-size: 18px;")
            self.cart_display.addWidget(item_label)  # Add to the cart section

        # Set maximum width for the cart display to prevent overflow
        self.cart_display.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)
        self.cart_display.setContentsMargins(5, 5, 5, 5)  # Add some margins to avoid widgets touching the edges

    def open_cart_popup(self):
        """Opens the cart popup window."""
        self.cart_popup = CartDetailWindow(self, self.update_cart_ui)  # Pass the callback to update cart UI when closed
        self.cart_popup.exec()

