import sys
from PyQt6.QtWidgets import QApplication
import view.main_window as mw  
import controller.controller as ctr  

"""
**Main File - Program Entry Point**

**Purpose:**
- This file serves as the main entry point for launching the application.
- Initializes the GUI and applies the global stylesheet.
- Instantiates the controller to manage interactions between views.

**Why This File Exists:**
- Ensures that the program starts with a properly configured GUI environment.
- Centralizes application initialization, making it easier to manage.
- Separates concerns by keeping GUI logic and event handling in their respective modules.

**Implementation Decisions:**
- Uses `QApplication` to initialize and manage the GUI event loop.
- Calls `load_stylesheet()` to apply a consistent theme to the entire application.
- Passes the controller instance to `MainWindow` to enable event handling.
"""

def load_stylesheet(app):
    """ Loads and applies the global stylesheet. """  
    with open("src/styles.css", "r") as f:  # Open CSS file and read
        app.setStyleSheet(f.read())  # Apply styles to the app

if __name__ == "__main__":
    """ Program Initialization """
    app = QApplication(sys.argv)  # Initialize QApplication
    load_stylesheet(app)  # Apply styles

    controller = ctr.Controller()  # Initialize the controller
    window = mw.MainWindow(controller)  # Create the main window
    window.show()  # Show the main window
    
    sys.exit(app.exec())  # Start the event loop
