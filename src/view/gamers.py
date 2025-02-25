from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
)
import sqlite3

class Registration(QWidget):
    """
    This class creates a registration form for the user to input their information and be registered
    with the cafe, allowing the user to sign up for events.
    """
    def __init__(self):
        """Initialize the registration form."""
        super().__init__()
        self.setWindowTitle("User Registration")
        self.setGeometry(300, 200, 400, 300)
        self.setup_ui()

    def setup_ui(self):
        """Set up the form layout and fields."""
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Form Fields
        self.fname_input = QLineEdit()
        self.lname_input = QLineEdit()
        self.gamertag_input = QLineEdit()
        self.email_input = QLineEdit()

        # Add Fields to Form Layout
        form_layout.addRow("First Name:", self.fname_input)
        form_layout.addRow("Last Name:", self.lname_input)
        form_layout.addRow("Gamer Tag:", self.gamertag_input)
        form_layout.addRow("Email:", self.email_input)

        # Buttons
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_user)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        # Add to Layout
        layout.addLayout(form_layout)
        layout.addWidget(self.register_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def register_user(self):
        """Handles user registration by checking uniqueness and storing in the database."""
        fname = self.fname_input.text().strip()
        lname = self.lname_input.text().strip()
        gamertag = self.gamertag_input.text().strip()
        email = self.email_input.text().strip()

        # Validate fields
        if not fname or not lname or not gamertag or not email:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        # Check if gamer tag or email already exists
        if self.check_gamertag_email(gamertag, email):
            QMessageBox.warning(self, "Error", "Gamer tag or email already exists!")
            return

        # Register user
        self.store_user(fname, lname, gamertag, email)

        # Let user know that they successfully registered
        QMessageBox.information(self, "Success", "User registered successfully!")

        # Clear the form after a successful registration
        self.fname_input.clear()
        self.lname_input.clear()
        self.gamertag_input.clear()
        self.email_input.clear()
        

    def check_gamertag_email(self, gamertag, email):
        """Checks if the gamertag or email already exists in the database."""
        conn = sqlite3.connect("src/game_cafe.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM registered_users WHERE gamertag = ? OR email = ?", (gamertag, email))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def store_user(self, fname, lname, gamertag, email):
        """Stores the new user in the database as a registered user."""
        conn = sqlite3.connect("src/game_cafe.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO registered_users (gamertag, fname, lname, email) VALUES (?, ?, ?, ?)",
            (gamertag, fname, lname, email)
        )
        conn.commit()
        conn.close()