from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy

class GameDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Library")
        self.setGeometry(100, 100, 900, 650)
        
        library_layout = QVBoxLayout()

        # Horizontal layout for the header of the menu and close button
        top_container = QHBoxLayout()
        # Header Label
        header_label = QLabel("Game Library")
        # Close Button
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        # Add widgets to top_container
        top_container.addWidget(header_label, 3)
        top_container.addWidget(close_button, 1)
        
        # Add the top layout to the main layout
        library_layout.addLayout(top_container) # Keep this in the first position to keep it at the top.
        
        self.setLayout(library_layout)
