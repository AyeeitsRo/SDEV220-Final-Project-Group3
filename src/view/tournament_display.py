from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy

class TournamentDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tournaments")
        self.setGeometry(100, 100, 900, 650)
        
        tournament_layout = QVBoxLayout()

        # Horizontal layout for the header of the menu and close button
        top_container = QHBoxLayout()
        # Header Label
        header_label = QLabel("Tournaments")
        # Close Button
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        # Add widgets to top_container
        top_container.addWidget(header_label, 3)
        top_container.addWidget(close_button, 1)
        
        # Add the top layout to the main layout    
        tournament_layout.addLayout(top_container) # Keep this in the first position to keep it at the top.


        self.setLayout(tournament_layout)