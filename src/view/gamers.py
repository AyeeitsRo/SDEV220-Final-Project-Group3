from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
)
import sqlite3

class Registration(QWidget):
    """
    **Registration Class**
    
    **Class Purpose:**
    - Provides a GUI form for users to register with the gaming cafe.
    - Stores user details in the database, allowing them to sign up for events.
    
    **Why This Class Exists:**
    - Ensures that only registered users can participate in events.
    - Validates user input and prevents duplicate registrations.
    - Automates the registration process and integrates with the database.
    """
    
    def __init__(self):
        """ Initializes the registration form UI. """
        super().__init__()  # Initialize QWidget
        self.setWindowTitle("User Registration")  # Set title
        self.setGeometry(300, 200, 400, 300)  # Set window size
        self.setup_ui()  # Load UI elements

    def setup_ui(self):
        """
        **Sets up the form layout and input fields.**
                
        **Why This Function Exists:**
        - Creates and structures the input fields and buttons.
        - Ensures the registration form follows a logical layout.
        - Connects buttons to their respective event handlers.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Create Layouts**
           - `QVBoxLayout()` for the main window layout.
           - `QFormLayout()` to structure form inputs.
        
        2️⃣ **Step 2 - Define Input Fields**
           - First name, last name, gamertag, and email fields.
        
        3️⃣ **Step 3 - Add Input Fields to Form Layout**
           - Uses `addRow()` to organize fields neatly.
        
        4️⃣ **Step 4 - Create Buttons**
           - Register button to submit user info.
           - Cancel button to close the window.
        
        5️⃣ **Step 5 - Add Components to Layouts**
           - Adds form layout and buttons to the main layout.
        """
        layout = QVBoxLayout()  # Step 1: Create the main layout
        form_layout = QFormLayout()  # Step 1: Create the form layout

        # Step 2: Define input fields
        self.fname_input = QLineEdit()  # Input for first name
        self.lname_input = QLineEdit()  # Input for last name
        self.gamertag_input = QLineEdit()  # Input for gamertag
        self.email_input = QLineEdit()  # Input for email

        # Step 3: Add fields to the form layout
        form_layout.addRow("First Name:", self.fname_input)
        form_layout.addRow("Last Name:", self.lname_input)
        form_layout.addRow("Gamer Tag:", self.gamertag_input)
        form_layout.addRow("Email:", self.email_input)

        # Step 4: Create buttons
        self.register_button = QPushButton("Register")  # Register button
        self.register_button.clicked.connect(self.register_user)  # Connects to register function
        
        self.cancel_button = QPushButton("Cancel")  # Cancel button
        self.cancel_button.clicked.connect(self.close)  # Closes window on click

        # Step 5: Add components to the layout
        layout.addLayout(form_layout)  # Adds form layout to main layout
        layout.addWidget(self.register_button)  # Adds register button
        layout.addWidget(self.cancel_button)  # Adds cancel button

        self.setLayout(layout)  # Applies layout to the widget

    def register_user(self):
        """
        **Handles user registration by validating and storing data.**
        **Why This Function Exists:**
        - Ensures users provide all necessary information before registering.
        - Prevents duplicate registrations by checking the database.
        - Stores valid user information into the database.
        - Clears the form after successful registration.
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Get User Input**
           - Retrieves text from input fields and removes extra spaces.
        
        2️⃣ **Step 2 - Validate Fields**
           - Ensures all fields are filled.
        
        3️⃣ **Step 3 - Check for Duplicate Entries**
           - Checks if the gamertag or email is already registered.
        
        4️⃣ **Step 4 - Store User in Database**
           - If valid, stores user data.
        
        5️⃣ **Step 5 - Display Success Message**
           - Notifies user of successful registration.
        
        6️⃣ **Step 6 - Clear Input Fields**
           - Resets the form after successful registration.
        """
        fname = self.fname_input.text().strip()  # Step 1: Get first name
        lname = self.lname_input.text().strip()  # Step 1: Get last name
        gamertag = self.gamertag_input.text().strip()  # Step 1: Get gamertag
        email = self.email_input.text().strip()  # Step 1: Get email

        # Step 2: Validate required fields
        if not fname or not lname or not gamertag or not email:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        # Step 3: Check if gamertag or email already exists
        if self.check_gamertag_email(gamertag, email):
            QMessageBox.warning(self, "Error", "Gamer tag or email already exists!")
            return

        # Step 4: Store user in the database
        self.store_user(fname, lname, gamertag, email)

        # Step 5: Show success message
        QMessageBox.information(self, "Success", "User registered successfully!")

        # Step 6: Clear input fields
        self.fname_input.clear()
        self.lname_input.clear()
        self.gamertag_input.clear()
        self.email_input.clear()
    
    def check_gamertag_email(self, gamertag: str, email: str) -> bool:
        """
        **Checks if a gamertag or email already exists in the database.**
        
        **Why This Function Exists:**
        - Ensures that each gamertag and email is unique to prevent duplicate registrations.
        - Helps maintain database integrity by preventing conflicts with existing users.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Connect to Database**
           - Establishes a connection to `game_cafe.db` to access user data.
        
        2️⃣ **Step 2 - Execute Query**
           - Uses a parameterized query to search for a user with the given gamertag or email.
           - Parameterized queries prevent SQL injection.
        
        3️⃣ **Step 3 - Check Query Results**
           - `fetchone()` checks if a matching record exists.
           - If a result is found, `exists` is set to `True`, otherwise `False`.
        
        4️⃣ **Step 4 - Close Connection**
           - Ensures database connection is properly closed after execution.
        
        5️⃣ **Step 5 - Return Result**
           - Returns `True` if a matching record exists, otherwise returns `False`.
        """
        conn = sqlite3.connect("src/game_cafe.db")  # Step 1: Connect to database
        cursor = conn.cursor()  # Step 1: Create cursor for executing SQL queries
        
        cursor.execute("SELECT 1 FROM registered_users WHERE gamertag = ? OR email = ?", (gamertag, email))  # Step 2: Execute query
        
        exists = cursor.fetchone() is not None  # Step 3: Check if query returned a result
        
        conn.close()  # Step 4: Close database connection
        return exists  # Step 5: Return True if found, False otherwise

    def store_user(self, fname: str, lname: str, gamertag: str, email: str) -> None:
        """
        **Stores the new user in the database as a registered user.**
        
        **Why This Function Exists:**
        - Saves user information into the database for future reference.
        - Allows registered users to participate in tournaments and events.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Connect to Database**
           - Establishes a connection to `game_cafe.db`.
        
        2️⃣ **Step 2 - Execute Insert Query**
           - Uses a parameterized query to safely insert user data into the database.
        
        3️⃣ **Step 3 - Commit Changes**
           - Ensures that the newly registered user is saved in the database.
        
        4️⃣ **Step 4 - Close Connection**
           - Closes the database connection to free up resources.
        """
        conn = sqlite3.connect("src/game_cafe.db")  # Step 1: Connect to database
        cursor = conn.cursor()  # Step 1: Create cursor
        
        cursor.execute(
            "INSERT INTO registered_users (gamertag, fname, lname, email) VALUES (?, ?, ?, ?)",
            (gamertag, fname, lname, email)
        )  # Step 2: Insert user data into the database
        
        conn.commit()  # Step 3: Save changes
        conn.close()  # Step 4: Close connection