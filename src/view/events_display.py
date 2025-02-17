from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt
from model.current_events import CurrentEvents

class EventsDisplay(QWidget):
    """
    A window that displays upcoming tournaments and campaign sessions for a specific game at the cafe.

    Attributes:
        game_name (str): The name of the game for which events are displayed.
        events (CurrentEvents): An instance of CurrentEvents used to fetch tournament and campaign data.
        main_layout (QVBoxLayout): The main layout of the window.
        event_layout (QVBoxLayout): The layout inside the scrollable area that contains event widgets.
    """

    def __init__(self, game_name, controller):
        """
        Initializes the event display for a specific game.

        Args:
            game_name (str): The name of the game for which events should be displayed.
        """
        super().__init__()
        self.controller = controller
        self.setWindowTitle(f"{game_name.capitalize()} - Events at the Cafe")
        self.setGeometry(200, 200, 500, 600)

        self.events = CurrentEvents()  # Load event data
        self.game_name = game_name

        # Main Layout
        self.main_layout = QVBoxLayout()

        # Header Label
        title_label = QLabel(f"{game_name.capitalize()} Events at the Cafe")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        self.main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Scrollable Area for Events
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        event_container = QWidget()
        self.event_layout = QVBoxLayout()
        event_container.setLayout(self.event_layout)
        scroll_area.setWidget(event_container)
        self.main_layout.addWidget(scroll_area)

        # Load and Display Events
        self.load_events()

        self.setLayout(self.main_layout)

    def load_events(self):
        """Loads tournaments and campaign sessions for the selected game and displays them in the UI."""
        tournaments = self.events.get_tournaments(self.game_name)
        campaigns = self.events.get_campaigns(self.game_name)

        if not tournaments and not campaigns:
            no_event_label = QLabel("No upcoming events at the cafe for this game.")
            no_event_label.setStyleSheet("font-size: 14px; color: gray;")
            self.event_layout.addWidget(no_event_label, alignment=Qt.AlignmentFlag.AlignCenter)
            return

        # Add tournaments to the UI
        for tournament in tournaments:
            event_widget = self.create_event_widget(tournament, event_type="tournament")
            self.event_layout.addWidget(event_widget)

        # Add campaign sessions to the UI
        for campaign in campaigns:
            event_widget = self.create_event_widget(campaign, event_type="campaign")
            self.event_layout.addWidget(event_widget)

    def create_event_widget(self, event, event_type):
        """
        Creates a widget for a tournament or campaign with a sign-up button.

        Args:
            event (dict): Dictionary containing event details.
            event_type (str): Either "tournament" or "campaign".

        Returns:
            QWidget: A styled widget displaying the event details.
        """
        frame = QFrame()
        frame.setStyleSheet("background-color: #201212; border: 2px solid #8b0000; border-radius: 10px; padding: 10px;")
        layout = QVBoxLayout()

        # Title
        title = QLabel(event["name"])
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ff5555;")
        layout.addWidget(title)

        # Date & Time
        date_time = QLabel(f"📅 {event['date']} at {event.get('time', 'TBA')}")
        date_time.setStyleSheet("font-size: 14px; color: #ffffff;")
        layout.addWidget(date_time)

        # Additional Details
        if event_type == "tournament":
            extra_info = QLabel(f"💰 Entry Fee: {event['entry_fee']} | 🏆 Prize: {event['prize']}")
        else:
            extra_info = QLabel(f"🎲 DM: {event['dm']} | 👥 Players Needed: {event['players_needed']}")
        extra_info.setStyleSheet("font-size: 13px; color: #cccccc;")
        layout.addWidget(extra_info)

        # Sign-Up Button
        signup_button = QPushButton("Sign Up")
        signup_button.setStyleSheet("""
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
        # Above is styled here due to css not styling instances/loops
        signup_button.clicked.connect(lambda: self.controller.on_signup(event, event_type))
        layout.addWidget(signup_button, alignment=Qt.AlignmentFlag.AlignCenter)

        frame.setLayout(layout)
        return frame


class AllEventsDisplay(QWidget):
    """
    A window that displays all upcoming tournaments and campaigns at the cafe.

    Attributes:
        events (CurrentEvents): An instance of CurrentEvents used to fetch event data.
        main_layout (QVBoxLayout): The main layout of the window.
        event_layout (QVBoxLayout): The layout inside the scrollable area that contains event widgets.
    """

    def __init__(self, controller):
        """Initializes the All Events display window."""
        super().__init__()
        self.controller = controller
        self.setWindowTitle("All Events at the Cafe")
        self.setGeometry(200, 200, 600, 700)

        self.events = CurrentEvents()  # Load all event data

        # Main Layout
        self.main_layout = QVBoxLayout()

        # Header
        title_label = QLabel("All Events at the Cafe")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        self.main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Scrollable Area for Events
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        event_container = QWidget()
        self.event_layout = QVBoxLayout()
        event_container.setLayout(self.event_layout)
        scroll_area.setWidget(event_container)
        self.main_layout.addWidget(scroll_area)

        # Load and Display Events
        self.load_all_events()
        self.setLayout(self.main_layout)

    def load_all_events(self):
        """Loads all tournaments and campaign sessions from CurrentEvents, grouped by game."""
        all_events = {}

        # Organize events by game
        for game, tournaments in self.events.tournaments.items():
            if game not in all_events:
                all_events[game] = []
            for t in tournaments:
                all_events[game].append((t, "tournament"))

        for game, campaigns in self.events.campaigns.items():
            if game not in all_events:
                all_events[game] = []
            for c in campaigns:
                all_events[game].append((c, "campaign"))

        if not all_events:
            no_event_label = QLabel("No upcoming events at the cafe.")
            no_event_label.setStyleSheet("font-size: 14px; color: gray;")
            self.event_layout.addWidget(no_event_label, alignment=Qt.AlignmentFlag.AlignCenter)
            return

        # Add events grouped by game
        for game, events in all_events.items():
            game_label = QLabel(game.capitalize())
            game_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ff5555; margin-top: 10px;")
            self.event_layout.addWidget(game_label)

            for event, event_type in events:
                event_widget = self.create_event_widget(event, event_type)
                self.event_layout.addWidget(event_widget)

    def create_event_widget(self, event, event_type):
        """Creates a widget for an event with a sign-up button."""
        frame = QFrame()
        frame.setStyleSheet("background-color: #201212; border: 2px solid #8b0000; border-radius: 10px; padding: 10px;")
        layout = QVBoxLayout()

        # Create Event UI (Similar to `EventsDisplay`)
        title = QLabel(event["name"])
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ff5555;")
        layout.addWidget(title)

        date_time = QLabel(f"📅 {event['date']} at {event.get('time', 'TBA')}")
        date_time.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(date_time)

        signup_button = QPushButton("Sign Up")
        signup_button.setStyleSheet("""
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
        # Above is styled here due to css not styling instances/loops
        signup_button.clicked.connect(lambda: self.controller.on_signup(event, event_type))
        layout.addWidget(signup_button, alignment=Qt.AlignmentFlag.AlignCenter)

        frame.setLayout(layout)
        return frame
