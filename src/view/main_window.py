from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QListWidget
from PyQt6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Gaming Cafe")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Sidebar (Profile and Active Sessions)r
        sidebar = QVBoxLayout()
        self.profile_label = QLabel("Welcome to the Gamer Cafe")
        self.profile_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.active_sessions = QListWidget()
        sidebar.addWidget(self.profile_label)
        sidebar.addWidget(self.active_sessions)
        
        # Main button area
        button_layout = QVBoxLayout()
        self.game_library_btn = QPushButton("Game Library")
        self.tournaments_btn = QPushButton("Tournaments")
        self.cafe_menu_btn = QPushButton("Café Menu")
        self.settings_btn = QPushButton("Settings")
        
        for btn, action in zip([self.game_library_btn, self.tournaments_btn, self.cafe_menu_btn, self.settings_btn],
                               [self.controller.open_game_library, self.controller.open_tournaments, self.controller.open_cafe_menu, self.controller.open_settings]):
            btn.setFont(QFont("Arial", 12))
            btn.setFixedHeight(50)
            btn.clicked.connect(action)
            button_layout.addWidget(btn)
        
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
