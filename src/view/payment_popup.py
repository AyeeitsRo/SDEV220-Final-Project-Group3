"""
File: payment_popup.py

Connects to cart_popup.py and serves as a popup window where the user chooses their method of payment.

Offers a choice between Cash and Credit/Debit.
If cash is chosen, it will notify the user that cash will be collected at the counter.
If credit/debit is chosen, it will provide the right fields to input card details for payment along with validation.
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLineEdit, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
import re

class PaymentWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Payment Options")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet("background-color: black; color: white;")

        layout = QVBoxLayout()

        # Payment option selector
        self.payment_method = QComboBox()
        self.payment_method.addItems(["Cash", "Debit/Credit"])
        layout.addWidget(self.payment_method)

        # Placeholder for payment input fields
        self.payment_input_layout = QVBoxLayout()
        layout.addLayout(self.payment_input_layout)

        # Initially hide debit/credit fields
        self.show_payment_fields()

        # Change the payment fields dynamically when the method changes
        self.payment_method.currentIndexChanged.connect(self.show_payment_fields)

        # Add a Pay button
        pay_button = QPushButton("Pay")
        pay_button.setStyleSheet("background-color: red; color: white; border-radius: 5px; padding: 10px;")
        pay_button.clicked.connect(self.pay)
        layout.addWidget(pay_button)

        self.setLayout(layout)

    def show_payment_fields(self):
        """Shows relevant fields based on the selected payment method."""
        # Clear any existing fields
        for i in range(self.payment_input_layout.count()):
            widget = self.payment_input_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Add fields based on the payment method
        if self.payment_method.currentText() == "Cash":
            # Display text for Cash option
            cash_message = QLabel("If Cash is selected,\nyour order will be sent to the counter to collect payment")
            cash_message.setStyleSheet("font-size: 16px; color: white; padding: 10px;")
            self.payment_input_layout.addWidget(cash_message)
        elif self.payment_method.currentText() == "Debit/Credit":
            # Card Number input
            self.payment_input_layout.addWidget(QLabel("*Card Number:"))
            self.card_number_input = QLineEdit()
            self.card_number_input.setValidator(self.create_card_number_validator())
            self.payment_input_layout.addWidget(self.card_number_input)

            # Expiration Date input
            self.payment_input_layout.addWidget(QLabel("*Expiration Date (MM/YY):"))
            self.expiration_date_input = QLineEdit()
            self.expiration_date_input.setValidator(self.create_expiration_date_validator())
            self.payment_input_layout.addWidget(self.expiration_date_input)

            # CVV input
            self.payment_input_layout.addWidget(QLabel("*CVV:"))
            self.cvv_input = QLineEdit()
            self.cvv_input.setValidator(self.create_cvv_validator())
            self.payment_input_layout.addWidget(self.cvv_input)

            # Name input
            self.payment_input_layout.addWidget(QLabel("*Name on Card:"))
            self.name_input = QLineEdit()
            self.payment_input_layout.addWidget(self.name_input)

    def create_card_number_validator(self):
        """Creates a validator for the card number."""
        regex = QRegularExpression(r'^\d{16}$')  # Validating a 16-digit card number
        return QRegularExpressionValidator(regex)

    def create_expiration_date_validator(self):
        """Creates a validator for the expiration date."""
        regex = QRegularExpression(r'^(0[1-9]|1[0-2])\/\d{2}$')  # Validating MM/YY format
        return QRegularExpressionValidator(regex)

    def create_cvv_validator(self):
        """Creates a validator for the CVV."""
        regex = QRegularExpression(r'^\d{3}$')  # Validating a 3-digit CVV
        return QRegularExpressionValidator(regex)

    def pay(self):
        """Handles the payment."""
        if self.payment_method.currentText() == "Cash":
            # For Cash: Show the message "Pay at the counter"
            self.show_popup("Thank you for your order!\nPlease pay at the counter.")  # Show the pop-up for Cash option
            self.accept()  # Close the window (or proceed as needed)
        elif self.payment_method.currentText() == "Debit/Credit":
            # For Debit/Credit: Proceed with card validation and payment
            card_number = self.card_number_input.text()
            expiration_date = self.expiration_date_input.text()
            cvv = self.cvv_input.text()
            name = self.name_input.text()

            # Validate all fields before processing payment
            if self.validate_fields(card_number, expiration_date, cvv, name):
                self.show_popup("Thank you for your order!\nIt is currently being made!")  # Show pop-up with customer's name
                self.accept()  # Proceed to payment processing (close the window)

    def validate_fields(self, card_number, expiration_date, cvv, name):
        """Validates the payment fields."""

        # Check if the card number is valid
        if len(card_number) != 16 or not card_number.isdigit():
            self.show_error_message("Card number must be 16 digits.")
            return False

        # Check if the expiration date is in MM/YY format (validating MM and YY)
        expiration_pattern = r"^(0[1-9]|1[0-2])\/\d{2}$"
        if not re.match(expiration_pattern, expiration_date):
            self.show_error_message("Expiration date must be in MM/YY format (e.g., 12/23).")
            return False

        # Check if the CVV is 3 digits
        if len(cvv) != 3 or not cvv.isdigit():
            self.show_error_message("CVV must be 3 digits.")
            return False

        # Check if the name field is filled out
        if not name:
            self.show_error_message("Name is required.")
            return False

        return True

    def show_popup(self, message):
        """Shows a popup message."""
        QMessageBox.information(self, "Payment Status", message)

    def show_error_message(self, message):
        """Displays an error message to the user."""
        QMessageBox.critical(self, "Invalid Input", message)
