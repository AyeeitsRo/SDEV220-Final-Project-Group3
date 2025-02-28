"""
File: cart_popup.py

Connects to menu.py and serves as a popup window before finalizing payment.

This window displays the user's cart of items along with each item's quantity and price.
It also calculates the total of all items in cart.
It allows for a user to make a last minute decision to delete an item from their cart and updates the total.
A return button allows for a user to return to the menu and add more items if they wish.
A pay button creates another popup window, "payment_popup.py"
"""

from model.order import *
from view.payment_popup import *
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, QSpacerItem, QSizePolicy

class CartDetailWindow(QDialog):
    def __init__(self, parent, close_callback):
        super().__init__(parent)
        self.setWindowTitle("Cart Details")
        self.setGeometry(150, 150, 400, 500)
        self.setStyleSheet("background-color: black;")

        self.close_callback = close_callback  # Save the callback to update the cart in the menu gui when closing
        
        # Layout for cart details
        self.cart_layout = QVBoxLayout()

        self.item_labels = []
        self.remove_buttons = []

        # Initially add all items in the order to the layout
        self.create_cart_items()

        # Spacer to push the total to the bottom
        self.bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.cart_layout.addItem(self.bottom_spacer)

        # Add a total label at the bottom
        self.total_label = QLabel(f"Total: ${float(order.add_total):.2f}")
        self.total_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.cart_layout.addWidget(self.total_label)

        # Create a horizontal layout for the return and pay buttons
        button_layout = QHBoxLayout()

        # Add the return button at the bottom left
        return_button = QPushButton("Return")
        return_button.setStyleSheet("background-color: red; color: white; border-radius: 5px; padding: 10px;")
        return_button.clicked.connect(self.close)  # Connect the return button to close the popup
        button_layout.addWidget(return_button)

        # Add the pay button at the bottom right
        pay_button = QPushButton("Pay")
        pay_button.setStyleSheet("background-color: red; color: white; border-radius: 5px; padding: 10px;")
        pay_button.clicked.connect(self.show_payment_options)  # Show the payment options popup
        button_layout.addWidget(pay_button)

        # Add the button layout to the cart layout
        self.cart_layout.addLayout(button_layout)

        self.setLayout(self.cart_layout)

    def create_cart_items(self):
        """Creates the items in the cart and adds them to the layout."""
        for item in order.items:
            item_layout = QHBoxLayout()

            item_label = QLabel(f"{item.name} - {item.quantity} x ${item.price:.2f}")
            item_label.setStyleSheet("color: white; font-size: 14px;")
            self.item_labels.append(item_label)
            item_layout.addWidget(item_label)

            remove_button = QPushButton("Remove Item")
            remove_button.setStyleSheet("background-color: red; color: white; border-radius: 5px; padding: 5px;")
            remove_button.clicked.connect(lambda checked, item=item, label=item_label: self.remove_item(item, label))
            self.remove_buttons.append(remove_button)
            item_layout.addWidget(remove_button)

            self.cart_layout.addLayout(item_layout)

    def remove_item(self, item, item_label):
        """Removes one quantity of the specified item from the cart and updates the UI."""
        if item.quantity > 1:
            item.quantity -= 1
        else:
            order.remove_item(item)
            self.remove_item_from_layout(item_label)

        item_label.setText(f"{item.name} - {item.quantity} x ${item.price:.2f}")
        self.total_label.setText(f"Total: ${float(order.add_total):.2f}")

    def remove_item_from_layout(self, item_label):
        """Removes the item and button from the layout."""
        for i in range(self.cart_layout.count()):
            layout_item = self.cart_layout.itemAt(i)
            if layout_item and isinstance(layout_item, QHBoxLayout):
                if item_label in [layout_item.itemAt(j).widget() for j in range(layout_item.count())]:
                    for j in range(layout_item.count()):
                        widget = layout_item.itemAt(j).widget()
                        if widget is not None:
                            widget.deleteLater()
                    break

        if not order.items:
            self.cart_layout.addWidget(QLabel("Cart is empty"))

    def show_payment_options(self):
        """Opens a payment options window."""
        payment_window = PaymentWindow(self)
        payment_window.exec()  # Open the payment window as a modal dialog

    def closeEvent(self, event):
        """Called when the popup is closed."""
        if self.close_callback:
            self.close_callback()  # Call the callback to notify the parent window
        event.accept()
