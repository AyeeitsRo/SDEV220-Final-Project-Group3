from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QListWidget
from PyQt6.QtGui import QFont, QIcon, QPixmap
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

        # Sidebar (Profile and Active Sessions)
        sidebar = QVBoxLayout()
        self.profile_label = QLabel("Welcome to the Gamer Cafe")
        self.profile_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.profile_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.active_sessions = QListWidget()
        sidebar.addWidget(self.profile_label)
        sidebar.addWidget(self.active_sessions)
        
        # Main button area with circular icons
        button_layout = QVBoxLayout()
        
        buttons = [
            ("Game Library", "resources\images\icon_library.png", "resources\images\library.png", self.controller.open_game_library),
            ("Tournaments", "tournament.png", "resources\images\icon_tournament.png", self.controller.open_tournaments),
            ("Café Menu", "cafe.png", "icon_cafe.png", self.controller.open_cafe_menu),
            ("Settings", "settings.png", "icon_settings.png", self.controller.open_settings)
        ]
        
        for text, icon, circle_icon, action in buttons:
            btn_layout = QVBoxLayout()
            
            icon_label = QLabel()
            icon_pixmap = QPixmap(circle_icon)
            icon_label.setPixmap(icon_pixmap.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setObjectName("circle-icon")  # Applying the CSS class
            
            btn = QPushButton(f" {text}")
            btn.setIcon(QIcon(icon))
            btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            btn.setFixedHeight(55)
            btn.clicked.connect(action)
            
            btn_layout.addWidget(icon_label)
            btn_layout.addWidget(btn)
            button_layout.addLayout(btn_layout)
        
        # Main layout
        main_layout.addLayout(sidebar, 2)  # Sidebar takes 2 parts
        main_layout.addLayout(button_layout, 3)  # Buttons take 3 parts

if __name__ == "__main__":
    from controller import Controller
    app = QApplication([])
    controller = Controller()
    window = MainWindow(controller)
    window.show()
    app.exec()
