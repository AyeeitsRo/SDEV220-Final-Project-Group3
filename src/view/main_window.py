from view.news_feed import NewsFeed
from model.current_events import CurrentEvents
from view.gamers import Registration
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, 
    QHBoxLayout, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QTimer
import sqlite3

class MainWindow(QMainWindow):
    """
    The main window of the Gaming Cafe application. Displays news, upcoming events, 
    and main navigation buttons for accessing different features.

    Attributes:
        controller (Controller): The main application controller.
        events (CurrentEvents): An instance of CurrentEvents to fetch event data.
        event_list (database query]): A list of upcoming events at the cafe.
        current_event_index (int): The index of the currently displayed event.
        timer (QTimer): Timer to cycle through events.
    """

    def __init__(self, controller):
        """
        Initializes the MainWindow.

        Args:
            controller (Controller): The application's main controller.
        """
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Gaming Cafe")
        self.setGeometry(100, 100, 900, 650)

        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Left side bar (Gaming news & active events)
        self.left_container = QWidget()
        left_side = QVBoxLayout(self.left_container)
        self.left_container.setStyleSheet("background-color: #201212; border: 3px solid #8b0000; border-radius: 10px; padding: 5px;")

        self.left_label = QLabel("Gaming News")
        self.left_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.left_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_label.setStyleSheet("background-color: transparent; border: none;")

        # News feed display
        self.news_feed = NewsFeed("https://feeds.feedburner.com/ign/games-all")  
        self.news_feed.setStyleSheet("border: none;")

        # Active Events mini display
        self.events_label = QLabel("Active / Upcoming Events")
        self.events_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.events_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.events_label.setStyleSheet("background-color: transparent; border: none;")
        self.active_events = QListWidget()
        self.active_events.setFixedWidth(400)
        self.active_events.setFixedHeight(150)        
        self.active_events.setStyleSheet("background-color: transparent; border: none;font-size: 24px; font-weight: bold; color: white;")
        # "View All Events" button
        self.events_btn = QPushButton("View All Events")
        self.events_btn.setStyleSheet("""
            QPushButton {
                background-color: #8b0000;
                color: white;
                border: 2px solid #ff3333;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a00000;
                border: 2px solid #ff5555;
            }
            QPushButton:pressed {
                background-color: #6a0000;
                border: 2px solid #cc0000;
            }
        """)
        self.events_btn.clicked.connect(self.controller.open_events)

        # Load events and set timer for cycling through them
        self.events = CurrentEvents()
        self.event_list = self.get_all_events()
        self.current_event_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_active_events)
        self.timer.start(5000)  # Switch event every 5 seconds
        self.update_active_events()

        # Add widgets to the left side
        left_side.addWidget(self.left_label)
        left_side.addWidget(self.news_feed)
        left_side.addWidget(self.events_label)
        left_side.addWidget(self.active_events, alignment=Qt.AlignmentFlag.AlignCenter)
        left_side.addWidget(self.events_btn)

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

            btn_layout.addWidget(icon_label)
            btn_layout.addWidget(btn)
            button_layout.addLayout(btn_layout)

        # Right sidebar (Login/sign up and additional features)
        self.right_container = QWidget()
        right_side = QVBoxLayout(self.right_container)
        self.right_container.setStyleSheet("background-color: #201212; border: 3px solid #8b0000; border-radius: 10px; padding: 5px;")

        self.right_label = QLabel("Register to Play!")
        self.right_label.setFont(QFont("Arial", 16, QFont.Weight.Light))
        self.right_label.setStyleSheet("background-color: transparent; border: none;")
        self.right_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.form = Registration()

        right_side.addWidget(self.right_label)
        right_side.addWidget(self.form)

        # Main layout
        main_layout.addWidget(self.left_container, 2)
        main_layout.addLayout(button_layout, 1)
        main_layout.addWidget(self.right_container, 2)

    def get_all_events(self):
        """
        Gets all active cafe-hosted events (tournaments & campaigns) from the database.
        """
        event_messages = []

        conn = sqlite3.connect("src/game_cafe.db")  # Relative path to database file
        cursor = conn.cursor()

        # Fetch all tournaments
        cursor.execute("SELECT event_name, game_type, event_type, date, time FROM active_tournaments")
        tournaments = cursor.fetchall()

        # Fetch all campaigns
        cursor.execute("SELECT campaign_name, game_type, host, meet_day, meet_frequency, time FROM active_campaigns")
        campaigns = cursor.fetchall()

        conn.close()

        # Format tournaments for display
        for event_name, game_type, event_type, date, time in tournaments:
            event_messages.append({
                "name": f"🎮\n{event_name}\n{date}\n{time}",
                "game_name": game_type
            })

        # Format campaigns for display
        for campaign_name, game_type, host, meet_day, meet_frequency, time in campaigns:
            event_messages.append({
                "name": f"📜\n{campaign_name}\n(DM: {host})\n{meet_day}, {meet_frequency} @ {time}",
                "game_name": game_type
            })
        # Format a message if there are not any active events for the chosen game
        return event_messages if event_messages else [{"name": "No upcoming events at the cafe.", "game_name": None}]


    def update_active_events(self):
        """
        Cycles through events and updates the QListWidget to display each event for a short duration.
        """
        self.active_events.clear()

        if self.event_list:
            event = self.event_list[self.current_event_index]

            # Create list item
            item = QListWidgetItem(event["name"])
            item.setData(Qt.ItemDataRole.UserRole, event["game_name"])  
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.active_events.addItem(item)

            # Cycle through events
            self.current_event_index = (self.current_event_index + 1) % len(self.event_list)

        # Ensure the item click event is connected only once, people be click happy
        if not hasattr(self, "event_connected"):
            self.active_events.itemClicked.connect(self.open_selected_event)
            self.event_connected = True 

    def open_selected_event(self, item):
        """
        Opens the event display window when an event is clicked.
        """
        game_name = item.data(Qt.ItemDataRole.UserRole)  
        if game_name:
            print(f"Opening events for: {game_name}")  # Debugging
            self.controller.on_game_clicked(game_name)
        else:
            QMessageBox.warning(self, "Error", "No game associated with this event.")
