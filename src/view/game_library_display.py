from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from model.game_library import GameLibrary  # Import GameLibrary class

class GameDisplay(QWidget):
    """
    A window that displays the Game Library, allowing users to browse games 
    categorized by type. Users can click on a game to view related events.

    Attributes:
        controller (Controller): The main controller that manages navigation.
        library_layout (QVBoxLayout): The main layout for the game library UI.
    """

    def __init__(self, controller):
        """
        Initializes the Game Library window.

        Args:
            controller (Controller): The application's main controller.
        """
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Game Library")
        self.setGeometry(100, 100, 900, 800)
        
        self.library_layout = QVBoxLayout()

        # --- Top Layout (Header + Close Button) ---
        top_container = QHBoxLayout()
        header_label = QLabel("Game Library")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
    
        top_container.addWidget(header_label, 3)
        top_container.addWidget(close_button, 1)

        self.library_layout.addLayout(top_container)  # Keep at the top

        # --- Load Games from GameLibrary into Scrollable Sections ---
        self.populate_games()

        self.setLayout(self.library_layout)

    def populate_games(self):
        """
        Populates the Game Library UI by grouping games into categories 
        and displaying them in scrollable sections.
        """
        game_lib = GameLibrary()
        games = game_lib.games

        # Step 1: Group games by category
        categorized_games = {}
        for game, details in games.items():
            category, image_path = details
            if category not in categorized_games:
                categorized_games[category] = []
            categorized_games[category].append((game, image_path))

        # Step 2: Create a scrollable section for each category
        for category, games_list in categorized_games.items():
            # --- Create Category Label ---
            category_label = QLabel(category.capitalize())  # Capitalize the category
            category_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
            self.library_layout.addWidget(category_label)

            # --- Create Scroll Area ---
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Hide vertical scroll
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Show horizontal scroll

            # Container for games (horizontal layout)
            game_container = QWidget()
            game_layout = QHBoxLayout()
            game_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Align games to the left
            game_container.setLayout(game_layout)

            # Step 3: Populate the category section with game images/titles
            for game_name, image_path in games_list:
                game_entry = self.create_game_entry(game_name, image_path)
                game_layout.addWidget(game_entry)

            # Step 4: Add game container to scroll area
            scroll_area.setWidget(game_container)
            self.library_layout.addWidget(scroll_area)

    def create_game_entry(self, game_name, image_path):
        """
        Creates a clickable game entry that includes an image and title button.

        Args:
            game_name (str): The name of the game.
            image_path (str): The file path to the game's image.

        Returns:
            QWidget: A widget containing the game entry with an image and title.
        """
        # Game thumbnail (as a button)
        game_button = QPushButton()
        pixmap = QPixmap(image_path)
        icon = QIcon(pixmap)
        game_button.setIcon(QIcon(pixmap))
        game_button.setIconSize(QSize(200, 200))  
        game_button.setStyleSheet("border: none;")  # Remove button borders

        # Game title (as a button)
        title_button = QPushButton(game_name.capitalize())
        title_button.setStyleSheet("color: #ffffff; font-size: 14px; text-align: center; border: none;")

        # Connect buttons to function in controller.py
        game_button.clicked.connect(lambda: self.controller.on_game_clicked(game_name))
        title_button.clicked.connect(lambda: self.controller.on_game_clicked(game_name))

        # Container layout
        game_entry = QVBoxLayout()
        game_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        game_entry.addWidget(game_button)
        game_entry.addWidget(title_button)

        # Game entry widget
        game_widget = QWidget()
        game_widget.setLayout(game_entry)

        return game_widget
