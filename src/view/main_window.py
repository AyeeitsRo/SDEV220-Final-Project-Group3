import sys
from view.news_feed import NewsFeed
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QListWidget
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Gaming Cafe")
        self.setGeometry(100, 100, 900, 650)

        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)



        # Left side bar (Gamer news / active events)
        self.left_container = QWidget()
        left_side = QVBoxLayout(self.left_container)
        self.left_container.setStyleSheet("background-color: #201212; border: 3px solid #8b0000; border-radius: 10px; padding: 5px;")
        self.left_label = QLabel("Gaming News")
        self.left_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.left_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_label.setStyleSheet("background-color: transparent; border: none;")
        self.news_feed = NewsFeed("https://feeds.feedburner.com/ign/games-all")  # IGN Gaming News Feed
        self.news_feed.setStyleSheet("border: none;")
        self.active_events = QListWidget()

        left_side.addWidget(self.left_label)
        left_side.addWidget(self.news_feed)
        left_side.addWidget(self.active_events)
        
        # Main button area with circular icons
        button_layout = QVBoxLayout()
        welcome_label = QLabel("Welcome to the Gamer Cafe!")
        welcome_label.setFont(QFont("Arial", 24, QFont.Weight.DemiBold))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # List of menu buttons
        buttons = [
            ("Game Library", "resources/images/icon_library.png", "resources/images/library.png", self.controller.open_game_library),
            ("Tournaments", "tournament.png", "resources/images/icon_tournament.png", self.controller.open_tournaments),
            ("Café Menu", "cafe.png", "resources/images/icon_cafe.png", self.controller.open_cafe_menu),
        ]
        
        for text, icon, circle_icon, action in buttons:
            btn_layout = QVBoxLayout()
            
            icon_label = QLabel()
            icon_pixmap = QPixmap(circle_icon)
            icon_label.setPixmap(icon_pixmap.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setObjectName("circle-icon")
            
            btn = QPushButton(f" {text}")
            btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            btn.setFixedHeight(55)
            btn.clicked.connect(action)
            
            btn_layout.addWidget(welcome_label)
            btn_layout.addWidget(icon_label)
            btn_layout.addWidget(btn)
            button_layout.addLayout(btn_layout)

        # Right sidebar (Login/sign up and Gamer joke of the day??)
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
        
        # Main layout
        main_layout.addWidget(self.left_container, 2)  # Sidebar takes 2 parts
        main_layout.addLayout(button_layout, 1)  # Buttons take 1 part
        main_layout.addWidget(self.right_container, 2)  # Sidebar takes 2 parts

if __name__ == "__main__":
    from controller import Controller
    app = QApplication([])
    controller = Controller()
    window = MainWindow(controller)
    window.show()
    app.exec()
