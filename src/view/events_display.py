from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from model.current_events import CurrentEvents
import sqlite3

class EventsDisplay(QWidget):
    """
    **A window that displays upcoming tournaments and campaign sessions.**

    **Why This Class Exists:**
    - Events are stored in a database and must be dynamically retrieved and displayed.
    - Users should be able to view upcoming tournaments and campaign sessions for a selected game.
    - The interface needs to support scrollable event listings to accommodate multiple entries.

    **Implementation Decisions:**
    - Uses a `QVBoxLayout` for structuring the event listings vertically.
    - A `QScrollArea` is used to ensure a smooth scrolling experience when many events exist.
    - The `CurrentEvents` model is used to retrieve relevant events based on the selected game.
    """

    def __init__(self, game_name: str, controller):
        """ Initializes the EventsDisplay window for a specific game."""

        super().__init__()  # Initialize the QWidget parent class

        # Store Class Attributes
        self.controller = controller  # Store controller instance
        self.game_name = game_name  # Store the game name for filtering events

        # Set Window Properties
        self.setWindowTitle(f"{game_name.capitalize()} - Events at the Cafe")  # Set dynamic window title
        self.setGeometry(200, 200, 500, 600)  # Define window size and position

        # Initialize Event Management
        self.events = CurrentEvents()  # Create instance to retrieve tournament and campaign data

        # Construct Main Layout
        self.main_layout = QVBoxLayout()  # Main layout for the event display

        # Create and Style the Header
        title_label = QLabel(f"{game_name.capitalize()} Events at the Cafe")  # Display game name in title
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")  # Style title
        self.main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Add title to layout

        # Set Up Scrollable Area
        scroll_area = QScrollArea()  # Create a scrollable area
        scroll_area.setWidgetResizable(True)  # Allow resizing of content
        event_container = QWidget()  # Container to hold event widgets
        self.event_layout = QVBoxLayout()  # Layout for organizing events
        event_container.setLayout(self.event_layout)  # Set container layout
        scroll_area.setWidget(event_container)  # Assign container to scroll area
        self.main_layout.addWidget(scroll_area)  # Add scrollable area to main layout

        # Load and Display Events
        self.load_events()  # Fetch events from the database and display them

        # Set the main layout for the widget
        self.setLayout(self.main_layout)  # Apply layout to the window


    def load_events(self):
        """
        **Loads tournaments and campaigns from the database and displays them in the UI.**

        **Why This Function Exists:**
        - Events (tournaments and campaigns) are stored in a database and must be dynamically retrieved.
        - This function ensures that only events related to the selected game are displayed.
        - If no events are found, an appropriate message is shown instead.

        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Retrieve Events from Database**
        - Calls `get_tournaments()` to fetch active tournaments for the selected game.
        - Calls `get_campaigns()` to fetch active campaigns for the selected game.

        2️⃣ **Step 2 - Check for Available Events**
        - If no tournaments or campaigns exist, display a message indicating that no events are available.

        3️⃣ **Step 3 - Add Tournaments to the UI**
        - Iterates through the list of retrieved tournaments.
        - Calls `create_event_widget()` to generate UI elements for each tournament.
        - Adds the generated tournament widget to the event layout.

        4️⃣ **Step 4 - Add Campaigns to the UI**
        - Iterates through the list of retrieved campaigns.
        - Calls `create_event_widget()` to generate UI elements for each campaign.
        - Adds the generated campaign widget to the event layout.
        """

        # Step 1 - Retrieve Events from Database
        tournaments = self.events.get_tournaments(self.game_name)  # Get all tournaments related to the game
        campaigns = self.events.get_campaigns(self.game_name)  # Get all campaigns related to the game

        # Step 2 - Check for Available Events
        if not tournaments and not campaigns:  # If both lists are empty
            no_event_label = QLabel("No upcoming events at the cafe for this game.")  # Create label for no events
            no_event_label.setStyleSheet("font-size: 14px; color: gray;")  # Style label
            self.event_layout.addWidget(no_event_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Add to UI
            return  # Exit function early since there are no events to display

        # Step 3 - Add Tournaments to the UI
        for tournament in tournaments:  # Loop through each retrieved tournament
            event_widget = self.create_event_widget(tournament, event_type="tournament")  # Create tournament UI element
            self.event_layout.addWidget(event_widget)  # Add tournament widget to event layout

        # Step 4 - Add Campaigns to the UI
        for campaign in campaigns:  # Loop through each retrieved campaign
            event_widget = self.create_event_widget(campaign, event_type="campaign")  # Create campaign UI element
            self.event_layout.addWidget(event_widget)  # Add campaign widget to event layout

def create_event_widget(self, event: dict, event_type: str) -> QFrame:
    """
    **Creates a UI widget for displaying a tournament or campaign event.**

    **Why This Function Exists:**
    - Each event must be visually distinct and formatted with relevant details.
    - The function dynamically formats event details based on event type (tournament or campaign).
    - Users should be able to sign up for an event directly from the UI.

    **Parameters:**
    - `event` (dict): A dictionary containing event details such as name, date, and additional information.
    - `event_type` (str): A string that specifies whether the event is a "tournament" or "campaign".

    **Returns:**
    - `QFrame`: A styled frame widget containing the formatted event information and a sign-up button.
        **Step-by-Step Breakdown:**
    1️⃣ **Step 1 - Create the Event Container**
       - Initializes a `QFrame` to visually separate each event in the UI.
       - Styles the frame with a dark background and a red border.

    2️⃣ **Step 2 - Create and Style the Layout**
       - Initializes a vertical layout (`QVBoxLayout`) to organize the event details.

    3️⃣ **Step 3 - Create and Style the Title**
       - Extracts the event name from the dictionary and displays it as a `QLabel`.
       - Applies bold styling and a red font color for visibility.

    4️⃣ **Step 4 - Format Event-Specific Details**
       - If the event is a **tournament**, it displays:
         - 📅 Date & Time
         - 💰 Entry Fee & 🏆 Prize
       - If the event is a **campaign**, it displays:
         - 📅 Meeting Day & Frequency
         - 🎲 Dungeon Master (DM) & 👥 Max Players

    5️⃣ **Step 5 - Style and Add Event Information**
       - Styles the event details and adds them to the layout.

    6️⃣ **Step 6 - Create and Style the Sign-Up Button**
       - Initializes a `QPushButton` labeled **"Sign Up"**.
       - Styles the button with a red theme and hover/press effects.

    7️⃣ **Step 7 - Connect the Button to the Controller**
       - Connects the sign-up button to `self.controller.on_signup()`.
       - Uses `lambda` to pass the event name and type when clicked.

    8️⃣ **Step 8 - Finalize and Return the Event Widget**
       - Sets the layout for the frame and returns the fully constructed widget.
    """

    # Step 1: Create a frame container to visually separate each event in the UI.
    frame = QFrame()
    frame.setStyleSheet("background-color: #201212; border: 2px solid #8b0000; border-radius: 10px; padding: 10px;")

    # Step 2: Create a vertical layout to hold event details within the frame.
    layout = QVBoxLayout()

    # Step 3: Create and style the title label, which displays the name of the event.
    title = QLabel(event["name"])  # Extract the event name from the dictionary.
    title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ff5555;")  # Apply styling for better readability.
    layout.addWidget(title)  # Add the title label to the layout.

    # Step 4: Display relevant event details based on whether it's a tournament or a campaign.
    if event_type == "tournament":
        # Format the event date and time with a calendar emoji.
        date_time = QLabel(f"\U0001F4C5 {event['date']} at {event['time']}")
        # Format additional details like entry fee and prize.
        extra_info = QLabel(f"\U0001F4B0 Entry Fee: {event['entry_fee']} | \U0001F3C6 Prize: {event['prize']}")
    else:
        # Format the campaign meeting schedule with a calendar emoji.
        date_time = QLabel(f"\U0001F4C5 {event['meet_day']} ({event['meet_frequency']}) at {event['time']}")
        # Format additional details like the Dungeon Master (DM) and max players.
        extra_info = QLabel(f"\U0001F3B2 DM: {event['host']} | \U0001F465 Max Players: {event['max_players']}")

    # Step 5: Style and add the event details to the layout.
    date_time.setStyleSheet("font-size: 14px; color: #ffffff;")  # Set font size and color for readability.
    extra_info.setStyleSheet("font-size: 13px; color: #cccccc;")  # Style additional details with a slightly smaller font.
    layout.addWidget(date_time)  # Add the date/time label to the layout.
    layout.addWidget(extra_info)  # Add the extra information label to the layout.

    # Step 6: Create and style the sign-up button.
    signup_button = QPushButton("Sign Up")  # Create a button labeled "Sign Up".
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
    """)  # Apply styling for a visually appealing button.

    # Step 7: Connect the button to the sign-up function in the controller.
    # - This lambda function passes the event name and type to the controller's `on_signup` method when clicked.
    signup_button.clicked.connect(lambda: self.controller.on_signup(event["name"], event_type))
    layout.addWidget(signup_button, alignment=Qt.AlignmentFlag.AlignCenter)  # Add the button to the layout and center it.

    # Step 8: Apply the layout to the frame and return it.
    frame.setLayout(layout)  # Set the layout for the event frame.
    return frame  # Return the fully constructed event widget.

class AllEventsDisplay(QWidget):
    """
    **A window that displays all upcoming tournaments and campaigns.**
    
    **Why This Class Exists:**
    - Provides a centralized UI for users to browse all scheduled tournaments and campaign sessions.
    - Dynamically loads event data from the database to ensure real-time updates.
    - Implements a scrollable interface to accommodate multiple events while maintaining a clean layout.
    
    **Attributes:**
    - `controller` (Controller): Handles event interactions and navigation.
    - `main_layout` (QVBoxLayout): The primary layout that organizes UI components.
    - `event_layout` (QVBoxLayout): Holds the dynamically generated event widgets.
    """

    def __init__(self, controller):
        """ Initializes the All Events display window. """
        super().__init__()  # Initialize the Parent Class
        self.controller = controller  # Store the Controller
        self.setWindowTitle("All Events at the Cafe")  # Configure Window Title
        self.setGeometry(200, 200, 800, 550)  # Set Window Dimensions

        # Create and Configure the Main Layout
        self.main_layout = QVBoxLayout()

        # Create and Style the Header
        title_label = QLabel("All Events at the Cafe")  # Create header label
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")  # Style header
        self.main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Add header to layout

        # Create and Configure the Scroll Area
        scroll_area = QScrollArea()  # Initialize scroll area
        scroll_area.setWidgetResizable(True)  # Allow dynamic resizing
        event_container = QWidget()  # Create container widget for events
        self.event_layout = QVBoxLayout()  # Create vertical layout for events
        event_container.setLayout(self.event_layout)  # Set event layout as container's layout
        scroll_area.setWidget(event_container)  # Assign container to scroll area
        self.main_layout.addWidget(scroll_area)  # Add scroll area to main layout

        # Load and Display Events from Database
        self.load_all_events()  # Retrieve and populate event listings
        self.setLayout(self.main_layout)  # Apply main layout to the window

    def load_all_events(self):
        """
        **Fetches and Displays All Upcoming Tournaments and Campaigns from the Database.**

        **Why This Function Exists:**
        - Events need to be dynamically fetched from the database to keep the UI updated.
        - Both tournaments and campaigns should be retrieved and displayed together.
        - Users should see all upcoming events available at the cafe.

        **Step-by-Step Breakdown:**
        1️⃣ **Step 1 - Connect to the Database**
           - Establishes a connection to the SQLite database where event data is stored.

        2️⃣ **Step 2 - Fetch Tournaments from the Database**
           - Retrieves all active tournaments from the `active_tournaments` table.

        3️⃣ **Step 3 - Fetch Campaigns from the Database**
           - Retrieves all active campaigns from the `active_campaigns` table.

        4️⃣ **Step 4 - Close the Database Connection**
           - Closes the connection to free up resources after fetching the data.

        5️⃣ **Step 5 - Handle Case Where No Events Exist**
           - If no tournaments or campaigns exist, display a message informing the user.

        6️⃣ **Step 6 - Populate the UI with Tournaments**
           - Iterates through the tournament data and creates widgets for each.

        7️⃣ **Step 7 - Populate the UI with Campaigns**
           - Iterates through the campaign data and creates widgets for each.
        """
        
        # Step 1 - Connect to the Database
        conn = sqlite3.connect("src/game_cafe.db")  # Establish database connection
        cursor = conn.cursor()  # Create a cursor object for executing SQL queries

        # Step 2 - Fetch Tournaments from the Database
        cursor.execute("""
            SELECT event_name, game_type, event_type, date, time, entry_fee, prize, max_players
            FROM active_tournaments
        """)
        tournaments = cursor.fetchall()  # Store retrieved tournament data

        # Step 3 - Fetch Campaigns from the Database
        cursor.execute("""
            SELECT campaign_name, game_type, host, meet_day, meet_frequency, time, max_players
            FROM active_campaigns
        """)
        campaigns = cursor.fetchall()  # Store retrieved campaign data

        # Step 4 - Close the Database Connection
        conn.close()  # Close the connection to free up resources

        # Step 5 - Handle Case Where No Events Exist
        if not tournaments and not campaigns:
            no_event_label = QLabel("No upcoming events at the cafe.")  # Create message label
            no_event_label.setStyleSheet("font-size: 14px; color: gray;")  # Style the message
            self.event_layout.addWidget(no_event_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Add to layout
            return  # Exit function since there are no events

        # Step 6 - Populate the UI with Tournaments
        for tournament in tournaments:
            event_widget = self.create_tournament_widget(tournament)  # Create a widget for each tournament
            self.event_layout.addWidget(event_widget)  # Add tournament widget to the UI

        # Step 7 - Populate the UI with Campaigns
        for campaign in campaigns:
            event_widget = self.create_campaign_widget(campaign)  # Create a widget for each campaign
            self.event_layout.addWidget(event_widget)  # Add campaign widget to the UI


    def create_tournament_widget(self, tournament):
        """
        **Creates a UI widget for a tournament with a sign-up button.**
        
        **Why This Function Exists:**
        - Provides a visually distinct widget for displaying tournament information.
        - Ensures a consistent UI format for tournaments.
        - Includes a sign-up button for user interaction.
        
        **Parameters:**
        - `tournament` (tuple): A tuple containing tournament details retrieved from the database, structured as:
            - `event_name` (str): Name of the tournament.
            - `game_type` (str): Type of game for the tournament.
            - `event_type` (str): Tournament format (e.g., "Single Elimination").
            - `date` (str): Date of the tournament.
            - `time` (str): Time of the tournament.
            - `entry_fee` (str): Cost to participate.
            - `prize` (str): Reward for winning.
            - `max_players` (int): Maximum number of participants.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Create UI Frame**
           - Initializes a `QFrame` to visually contain the tournament details.
           - Applies a dark red theme with a border to match the UI style.
        
        2️⃣ **Step 2 - Extract Tournament Data**
           - Unpacks the tournament tuple into individual variables.
        
        3️⃣ **Step 3 - Create and Style Title Label**
           - Displays the tournament name in bold red text.
        
        4️⃣ **Step 4 - Display Date & Time**
           - Shows when the tournament will take place.
        
        5️⃣ **Step 5 - Display Additional Tournament Info**
           - Includes game type, tournament format, entry fee, prize, and max players.
        
        6️⃣ **Step 6 - Create and Style Sign-Up Button**
           - Users can click this button to sign up for the tournament.
           - Uses hover and pressed effects to provide feedback.
        
        7️⃣ **Step 7 - Return the Completed Tournament Widget**
           - Combines all components into a single `QFrame` and returns it.
        """
        
        # Step 1 - Create UI Frame
        frame = QFrame()
        frame.setStyleSheet("background-color: #201212; border: 2px solid #8b0000; border-radius: 10px; padding: 10px;")
        layout = QVBoxLayout()
        
        # Step 2 - Extract Tournament Data
        event_name, game_type, event_type, date, time, entry_fee, prize, max_players = tournament
        
        # Step 3 - Create and Style Title Label
        title = QLabel(event_name)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ff5555;")
        layout.addWidget(title)
        
        # Step 4 - Display Date & Time
        date_time = QLabel(f"\U0001F4C5 {date} at {time}")  # Unicode for 📅
        date_time.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(date_time)
        
        # Step 5 - Display Additional Tournament Info
        extra_info = QLabel(f"\U0001F3AE {game_type} | \U0001F3C6 {event_type} | \U0001F4B0 Entry Fee: {entry_fee} | Prize: {prize} | Max Players: {max_players}")
        extra_info.setStyleSheet("font-size: 13px; color: #cccccc;")
        layout.addWidget(extra_info)
        
        # Step 6 - Create and Style Sign-Up Button
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
        
        # Step 7 - Return the Completed Tournament Widget
        frame.setLayout(layout)
        return frame

    def create_campaign_widget(self, campaign):
        """
        **Creates a UI widget for a campaign session with a sign-up button.**
        
        **Why This Function Exists:**
        - Provides a visually distinct widget for displaying campaign details.
        - Ensures a consistent UI format for campaign sessions.
        - Includes a sign-up button for user interaction.
        
        **Parameters:**
        - `campaign` (tuple): A tuple containing campaign details retrieved from the database, structured as:
            - `campaign_name` (str): Name of the campaign.
            - `game_type` (str): Type of game for the campaign.
            - `host` (str): Name of the Dungeon Master (DM) or campaign host.
            - `meet_day` (str): Day of the week the campaign meets.
            - `meet_frequency` (str): Frequency of the meetings (e.g., weekly, biweekly).
            - `time` (str): Time the campaign session starts.
            - `max_players` (int): Maximum number of participants allowed.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Create UI Frame**
           - Initializes a `QFrame` to visually contain the campaign details.
           - Applies a dark red theme with a border to match the UI style.
        
        2️⃣ **Step 2 - Extract Campaign Data**
           - Unpacks the campaign tuple into individual variables.
        
        3️⃣ **Step 3 - Create and Style Title Label**
           - Displays the campaign name in bold red text.
        
        4️⃣ **Step 4 - Display Meeting Schedule**
           - Shows when and how frequently the campaign meets.
        
        5️⃣ **Step 5 - Display Additional Campaign Info**
           - Includes game type, Dungeon Master (DM), and max players.
        
        6️⃣ **Step 6 - Create and Style Sign-Up Button**
           - Users can click this button to sign up for the campaign.
           - Uses hover and pressed effects to provide feedback.
        
        7️⃣ **Step 7 - Return the Completed Campaign Widget**
           - Combines all components into a single `QFrame` and returns it.
        """
        
        # Step 1 - Create UI Frame
        frame = QFrame()
        frame.setStyleSheet("background-color: #201212; border: 2px solid #8b0000; border-radius: 10px; padding: 10px;")
        layout = QVBoxLayout()
        
        # Step 2 - Extract Campaign Data
        campaign_name, game_type, host, meet_day, meet_frequency, time, max_players = campaign
        
        # Step 3 - Create and Style Title Label
        title = QLabel(campaign_name)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ff5555;")
        layout.addWidget(title)
        
        # Step 4 - Display Meeting Schedule
        date_time = QLabel(f"\U0001F5D3 {meet_day}, {meet_frequency} | \U0001F550 {time}")  # Unicode for 🗓 ⏰
        date_time.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(date_time)
        
        # Step 5 - Display Additional Campaign Info
        extra_info = QLabel(f"\U0001F3B2 {game_type} | \U0001F3C5 DM: {host} | \U0001F465 Players Needed: {max_players}")
        extra_info.setStyleSheet("font-size: 13px; color: #cccccc;")
        layout.addWidget(extra_info)
        
        # Step 6 - Create and Style Sign-Up Button
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
        
        # Step 7 - Return the Completed Campaign Widget
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
