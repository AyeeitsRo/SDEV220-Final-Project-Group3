from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from model.game_library import GameLibrary  # Import GameLibrary class

class GameDisplay(QWidget):
    """
    **Displays the Game Library, allowing users to browse available games.**

    **Why This Class Exists:**
    - Provides users with a visual interface to explore available games at the café.
    - Organizes games into categories using `GameLibrary`.
    - Allows users to click on a game to view related events.

    **Implementation Decisions:**
    - Uses a `QVBoxLayout` for vertical organization of UI elements.
    - Includes a scrollable section to accommodate a growing list of games.
    - Retrieves game data dynamically from `GameLibrary`.
    """

    def __init__(self, controller):
        """ Initializes the Game Library window. """
        super().__init__()
        self.controller = controller  # Store the controller instance
        self.setWindowTitle("Game Library")  # Set window title
        self.setGeometry(100, 100, 900, 800)  # Set window size
        
        self.library_layout = QVBoxLayout()  # Create main layout

        # Create Header Section 
        top_container = QHBoxLayout()  # Create horizontal layout for header
        
        header_label = QLabel("Game Library")  # Create title label
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")  # Style title
        
        close_button = QPushButton("Close")  # Create close button
        close_button.clicked.connect(self.close)  # Connect close button to exit function
    
        top_container.addWidget(header_label, 3)  # Add title with weight for spacing
        top_container.addWidget(close_button, 1)  # Add close button

        self.library_layout.addLayout(top_container)  # Add header section to main layout

        # Load Games from GameLibrary
        self.populate_games()

        # Set Final Layout
        self.setLayout(self.library_layout)

    def populate_games(self):
        """
        **Populates the Game Library UI by grouping games into categories 
        and displaying them in scrollable sections.**

        **Why This Function Exists:**
        - The game library must be dynamically generated from `GameLibrary`, ensuring all games are displayed.
        - Games are categorized based on their type (e.g., "competitive", "campaign") to improve readability.
        - Each category section needs to be scrollable for better navigation.

        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Retrieve and Organize Game Data**
           - Fetches all games from `GameLibrary`.
           - Groups them into categories.

        2️⃣ **Step 2 - Create Scrollable Sections for Each Category**
           - Labels each category.
           - Creates a horizontal scroll area for the games.

        3️⃣ **Step 3 - Populate Each Category with Game Entries**
           - Loads each game's name and image.
           - Adds them to the corresponding category section.

        4️⃣ **Step 4 - Display the Scrollable Sections**
           - Adds the scrollable container to the main layout.
        """
        
        game_lib = GameLibrary()  # Step 1: Create an instance of GameLibrary to access stored game data.
        games = game_lib.games  # Retrieve the dictionary containing all game information.

        # Step 1 - Group games by category
        categorized_games = {}  # Dictionary to store games categorized by type.
        for game, details in games.items():
            category, image_path = details  # Extract the category and image path for each game.
            if category not in categorized_games:  # If the category doesn't exist, create an entry.
                categorized_games[category] = []
            categorized_games[category].append((game, image_path))  # Append the game to its respective category.

        # Step 2 - Create a scrollable section for each category
        for category, games_list in categorized_games.items():
            # --- Create Category Label ---
            category_label = QLabel(category.capitalize())  # Capitalize and display the category name.
            category_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")  # Style the label.
            self.library_layout.addWidget(category_label)  # Add the label to the main layout.

            # --- Create Scroll Area ---
            scroll_area = QScrollArea()  # Create a scrollable container.
            scroll_area.setWidgetResizable(True)  # Allow resizing to fit content dynamically.
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Hide vertical scroll (not needed).
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Show horizontal scroll if needed.

            # Step 3 - Create a container for games with horizontal layout
            game_container = QWidget()  # Create a widget to hold the game entries.
            game_layout = QHBoxLayout()  # Create a horizontal layout to arrange games in a row.
            game_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Align all game widgets to the left.
            game_container.setLayout(game_layout)  # Apply the layout to the container.

            # Step 3 - Populate the category section with game images/titles
            for game_name, image_path in games_list:
                game_entry = self.create_game_entry(game_name, image_path)  # Create a game entry widget.
                game_layout.addWidget(game_entry)  # Add the game entry widget to the layout.

            # Step 4 - Add the game container to the scroll area
            scroll_area.setWidget(game_container)  # Set the game container inside the scrollable area.
            self.library_layout.addWidget(scroll_area)  # Add the scrollable section to the main layout.

    def create_game_entry(self, game_name: str, image_path: str) -> QWidget:
        """
        **Creates a clickable game entry that includes an image and title button.**

        **Why This Function Exists:**
        - Each game in the Game Library must be displayed as an interactive entry.
        - A game entry consists of an image (icon) and a title button.
        - Users should be able to click on either element to open the associated game events.

        **Parameters:**
        - `game_name` (str): The name of the game.
        - `image_path` (str): The file path to the game's image.

        **Returns:**
        - `QWidget`: A widget containing the game entry with an image and title.

        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Create a Clickable Image Button**
           - Loads the game's image and sets it as a button icon.
        
        2️⃣ **Step 2 - Create a Clickable Title Button**
           - Displays the game's name as a button with a clean design.
        
        3️⃣ **Step 3 - Connect Click Events to the Controller**
           - Clicking either the image or the title should trigger `on_game_clicked()`.
        
        4️⃣ **Step 4 - Arrange Buttons in a Vertical Layout**
           - Stack the image and title in a centered column.
        
        5️⃣ **Step 5 - Return the Game Entry as a QWidget**
           - The final widget is returned to be placed inside the Game Library UI.
        """

        # Step 1 - Create a Clickable Image Button
        game_button = QPushButton()  # Create a QPushButton for the game image
        pixmap = QPixmap(image_path)  # Load the image from the given file path
        icon = QIcon(pixmap)  # Convert the pixmap into an icon format
        game_button.setIcon(QIcon(pixmap))  # Set the button's icon as the game image
        game_button.setIconSize(QSize(200, 200))  # Resize the icon to fit within 200x200 pixels
        game_button.setStyleSheet("border: none;")  # Remove any default button borders

        # Step 2 - Create a Clickable Title Button
        title_button = QPushButton(game_name.capitalize())  # Display game name with first letter capitalized
        title_button.setStyleSheet("color: #ffffff; font-size: 14px; text-align: center; border: none;")  # Style the text

        # Step 3 - Connect Click Events to the Controller
        # Both the game image and title button should trigger `on_game_clicked()`
        game_button.clicked.connect(lambda: self.controller.on_game_clicked(game_name))  # Image button click event
        title_button.clicked.connect(lambda: self.controller.on_game_clicked(game_name))  # Title button click event

        # Step 4 - Arrange Buttons in a Vertical Layout
        game_entry = QVBoxLayout()  # Create a vertical layout to hold the buttons
        game_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align the layout elements
        game_entry.addWidget(game_button)  # Add the game image button
        game_entry.addWidget(title_button)  # Add the game title button

        # Step 5 - Return the Game Entry as a QWidget
        game_widget = QWidget()  # Create a QWidget to hold the layout
        game_widget.setLayout(game_entry)  # Apply the vertical layout to the widget

        return game_widget  # Return the complete game entry widget
