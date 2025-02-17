import sys
from PyQt6.QtWidgets import QApplication
import view.main_window as mw  
import controller.controller as ctr 

"""
This is the main file from which the program runs
"""

def load_stylesheet(app):
    """ Opens styles.css, which creates a template for generalized styling through out the GUI """
    with open("src/styles.css", "r") as f: # Open css file and read
        app.setStyleSheet(f.read())  # Apply styles to the app

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Initialize QApplication
    load_stylesheet(app)  # Apply styles

    controller = ctr.Controller()  # Initialize the controller
    window = mw.MainWindow(controller)  # Create the window with controller
    window.show()  # Show the main window
    
    sys.exit(app.exec())  # Start the event loop

