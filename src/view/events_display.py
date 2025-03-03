from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from model.current_events import CurrentEvents
import sqlite3

class EventsDisplay(QWidget):
    """
    A window that displays upcoming tournaments and campaign sessions
    """

    def __init__(self, game_name, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle(f"{game_name.capitalize()} - Events at the Cafe")
        self.setGeometry(200, 200, 500, 600)

        self.events = CurrentEvents()  # Load events from the database
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
        """Loads tournaments and campaigns from the database and displays them."""
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
        """Creates a UI widget for a tournament or campaign."""
        frame = QFrame()
        frame.setStyleSheet("background-color: #201212; border: 2px solid #8b0000; border-radius: 10px; padding: 10px;")
        layout = QVBoxLayout()

        # Title
        title = QLabel(event["name"])
        
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ff5555;")
        layout.addWidget(title)

        # Extra Information
        if event_type == "tournament":
            date_time = QLabel(f"📅 {event['date']} at {event['time']}")
            extra_info = QLabel(f"💰 Entry Fee: {event['entry_fee']} | 🏆 Prize: {event['prize']}")
        else:
            date_time = QLabel(f"📅 {event['meet_day']}({event['meet_frequency']}) at {event['time']}")
            extra_info = QLabel(f"🎲 DM: {event['host']} | 👥 Max Players: {event['max_players']}")
        date_time.setStyleSheet("font-size: 14px; color: #ffffff;")
        layout.addWidget(date_time)
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
        signup_button.clicked.connect(lambda: self.controller.on_signup(event["name"], event_type))
        layout.addWidget(signup_button, alignment=Qt.AlignmentFlag.AlignCenter)

        frame.setLayout(layout)
        return frame

class AllEventsDisplay(QWidget):
    """
    A window that displays all upcoming tournaments and campaigns.
    """

    def __init__(self, controller):
        """Initializes the All Events display window."""
        super().__init__()
        self.controller = controller
        self.setWindowTitle("All Events at the Cafe")
        self.setGeometry(200, 200, 800, 550)

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

        # Load and Display Events from Database
        self.load_all_events()
        self.setLayout(self.main_layout)

    def load_all_events(self):
        """Loads all tournaments and campaigns from the database."""
        conn = sqlite3.connect("src/game_cafe.db")
        cursor = conn.cursor()

        # Fetch all active tournaments
        cursor.execute("SELECT event_name, game_type, event_type, date, time, entry_fee, prize, max_players FROM active_tournaments")
        tournaments = cursor.fetchall()

        # Fetch all active campaigns
        cursor.execute("SELECT campaign_name, game_type, host, meet_day, meet_frequency, time, max_players FROM active_campaigns")
        campaigns = cursor.fetchall()

        conn.close()

        if not tournaments and not campaigns:
            no_event_label = QLabel("No upcoming events at the cafe.")
            no_event_label.setStyleSheet("font-size: 14px; color: gray;")
            self.event_layout.addWidget(no_event_label, alignment=Qt.AlignmentFlag.AlignCenter)
            return

        # Add tournaments to UI
        for tournament in tournaments:
            event_widget = self.create_tournament_widget(tournament)
            self.event_layout.addWidget(event_widget)

        # Add campaigns to UI
        for campaign in campaigns:
            event_widget = self.create_campaign_widget(campaign)
            self.event_layout.addWidget(event_widget)

    def create_tournament_widget(self, tournament):
        """Creates a widget for a tournament with a sign-up button."""
        frame = QFrame()
        frame.setStyleSheet("background-color: #201212; border: 2px solid #8b0000; border-radius: 10px; padding: 10px;")
        layout = QVBoxLayout()

        event_name, game_type, event_type, date, time, entry_fee, prize, max_players = tournament

        # Title
        title = QLabel(event_name)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ff5555;")
        layout.addWidget(title)

        # Date & Time
        date_time = QLabel(f"📅 {date} at {time}")
        date_time.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(date_time)

        # Extra Info
        extra_info = QLabel(f"🎮 {game_type} | 🏆 {event_type} | 💰 Entry Fee: {entry_fee} | Prize: {prize} | Max Players: {max_players}")
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
        signup_button.clicked.connect(lambda: self.controller.on_signup(event_name, "tournament"))
        layout.addWidget(signup_button, alignment=Qt.AlignmentFlag.AlignCenter)

        frame.setLayout(layout)
        return frame

    def create_campaign_widget(self, campaign):
        """Creates a widget for a campaign session with a sign-up button."""
        frame = QFrame()
        frame.setStyleSheet("background-color: #201212; border: 2px solid #8b0000; border-radius: 10px; padding: 10px;")
        layout = QVBoxLayout()

        campaign_name, game_type, host, meet_day, meet_frequency, time, max_players = campaign

        # Title
        title = QLabel(campaign_name)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ff5555;")
        layout.addWidget(title)

        # Date & Time
        date_time = QLabel(f"🗓 {meet_day}, {meet_frequency} | ⏰ {time}")
        date_time.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(date_time)

        # Extra Info
        extra_info = QLabel(f"🎲 {game_type} | 🏅 DM: {host} | 👥 Players Needed: {max_players}")
        # TODO: Retrieve list of players who are already signed up. Replace Players Needed to reflect max_players - current_players
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
        signup_button.clicked.connect(lambda: self.controller.on_signup(campaign_name, "campaign"))
        layout.addWidget(signup_button, alignment=Qt.AlignmentFlag.AlignCenter)

        frame.setLayout(layout)
        return frame

class EventSignUp(QWidget):
    """
    This class creates a small window with an input method for users to enter their gamertag to sign up for events.
    It checks the database for existing users and updates the database with successful registrations.
    """

    def __init__(self, controller, event_name, event_type):
        """Initialize the sign-up form."""
        super().__init__()
        self.controller = controller
        self.event_name = event_name
        self.event_type = event_type
        self.setWindowTitle("User Registration")
        self.setGeometry(300, 200, 400, 300)
        self.setup_ui()

    def setup_ui(self):
        """Sets up the UI elements."""
        self.layout = QVBoxLayout(self)
        signup_label = QLabel("Enter your gamertag to Sign Up!")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter gamertag here...")

        # Buttons
        signup_button = QPushButton("Sign Up")
        signup_button.clicked.connect(self.sign_up)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)

        self.layout.addWidget(signup_label)
        self.layout.addWidget(self.search_input)
        self.layout.addWidget(signup_button)
        self.layout.addWidget(cancel_button)

    def sign_up(self):
        """Handles sign-up logic."""
        gamertag = self.search_input.text().strip()

        # Make sure the field is filled out
        if not gamertag:
            QMessageBox.warning(self, "Error", "Gamertag cannot be empty!")
            return

        # Get user_id from registered_users
        user_id = self.get_user_id(gamertag)

        if user_id is None:
            QMessageBox.warning(self, "Error", "Gamertag not found. Please register first.")
            return

        # Attempt to add user to event
        self.add_user_to_event(user_id)

    def get_user_id(self, gamertag):
        """Retrieves user_id from registered_users based on gamertag."""
        conn = sqlite3.connect("src/game_cafe.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM registered_users WHERE gamertag = ?", (gamertag,))
        user_id = cursor.fetchone()
        conn.close()
        return user_id[0] if user_id else None  # Returns user_id if found

    def add_user_to_event(self, user_id):
        """Adds the user to the selected event."""
        conn = sqlite3.connect("src/game_cafe.db")
        cursor = conn.cursor()

        # Check current signups for the event
        cursor.execute("SELECT COUNT(*) FROM event_signup WHERE event_name = ?", (self.event_name,))
        current_signups = cursor.fetchone()[0]

        # Get max_players for this event
        cursor.execute("SELECT max_players FROM active_tournaments WHERE event_name = ?", (self.event_name,))
        max_players = cursor.fetchone()

        if max_players is None:
            QMessageBox.warning(self, "Error", "Event not found!")
            conn.close()
            return

        max_players = int(max_players[0])  # Extract integer value

        # Check if event is full
        if current_signups >= max_players:
            QMessageBox.warning(self, "Error", "This event is already full!")
            conn.close()
            return

        # Check if user is already signed up
        cursor.execute("SELECT 1 FROM event_signup WHERE gamertag = ? AND event_name = ?", (user_id, self.event_name))
        if cursor.fetchone():
            QMessageBox.warning(self, "Error", "You are already signed up for this event!")
            conn.close()
            return

        # Insert into signups table
        cursor.execute("INSERT INTO event_signup (gamertag, event_name) VALUES (?, ?)", (user_id, self.event_name))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", f"Successfully signed up for {self.event_name}!")
        self.close()
