from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, 
    QTableWidgetItem, QFrame, QHeaderView, QScrollArea
)
from PyQt6.QtCore import Qt
from model.current_events import CurrentEvents
from model.tournament import *


class TournamentDisplay(QWidget):
    """
    **Class Purpose:**
    - Displays all active tournaments in the GUI.
    - Retrieves tournament data dynamically from `CurrentEvents` (database).
    - Allows users to view tournament brackets and match details.
    
    **Why This Class Exists:**
    - Tournaments must be dynamically displayed as they are stored and updated in the database.
    - Users need an interface to see active tournaments and interact with them.
    
    **Implementation Decisions:**
    - Uses a vertical layout to list tournaments.
    - Fetches data dynamically from `CurrentEvents` to ensure the latest tournaments are displayed.
    """
    def __init__(self, controller):
        """
        **Initializes the TournamentDisplay window.**

        **Parameters:**
        - `controller`: The main application controller for managing UI transitions.
        """
        super().__init__()
        self.controller = controller  # Store the controller instance for managing navigation
        self.setWindowTitle("Tournaments")  # Set the window title
        self.setGeometry(100, 100, 900, 650)  # Define window size and position
        
        # Create the main vertical layout container that will hold all UI elements
        self.tournament_layout = QVBoxLayout()

        # --- Header Section ---
        # Create a horizontal layout for the header
        top_container = QHBoxLayout()
        
        # Create and style the title label
        header_label = QLabel("Tournaments")  # Displayed title text
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        # Create a Close button to exit the tournament display window
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)  # Connect button click to close action
        
        # Add elements to the header layout with a 3:1 ratio for spacing
        top_container.addWidget(header_label, 3)
        top_container.addWidget(close_button, 1)
        
        # Add the header layout to the main vertical layout
        self.tournament_layout.addLayout(top_container)

        # Load the list of tournaments dynamically from `CurrentEvents`
        self.load_tournaments()

        # Set the final layout of the widget to the constructed layout
        self.setLayout(self.tournament_layout)

    def load_tournaments(self) -> None:
        """
        **Retrieves and displays all active tournaments.**
        
        **Why This Function Exists:**
        - Tournament data is stored in the database and needs to be dynamically fetched.
        - Ensures that the latest tournaments are displayed in real-time.
        - If no tournaments are available, a message is shown to inform users.
        
        **Implementation Decisions:**
        - Calls `CurrentEvents` to get the latest tournament data.
        - If no tournaments are found, a placeholder message is displayed.
        - If tournaments exist, it dynamically creates and adds widgets for each tournament.
        
        **Parameters:**
        - None.
        
        **Returns:**
        - None. This function modifies the UI by adding tournament widgets.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Fetch Tournament Data**
           - Creates an instance of `CurrentEvents` to retrieve stored tournaments.
        
        2️⃣ **Step 2 - Retrieve All Tournaments**
           - Calls `get_all_tournaments()` to obtain tournament data.
        
        3️⃣ **Step 3 - Check if Tournaments Exist**
           - If no tournaments exist, displays a message to inform users.
        
        4️⃣ **Step 4 - Create Tournament Widgets**
           - If tournaments exist, iterates through them and creates UI widgets.
        """
        
        # Step 1 - Fetch Tournament Data
        self.events = CurrentEvents()  # Create an instance of CurrentEvents to retrieve tournament data
        
        # Step 2 - Retrieve All Tournaments
        all_tournaments = self.events.get_all_tournaments()  # Fetch all stored tournaments from the database
        
        # Step 3 - Check if Tournaments Exist
        if not all_tournaments:  # If the list of tournaments is empty
            no_tournaments = QLabel("No tournaments currently available.")  # Create a label for displaying the message
            no_tournaments.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align the message
            no_tournaments.setStyleSheet("font-size: 16px; color: gray;")  # Style the message text
            self.tournament_layout.addWidget(no_tournaments)  # Add the message to the UI layout
            return  # Exit the function as there are no tournaments to display
        
        # Step 4 - Create Tournament Widgets
        for tournament in all_tournaments:  # Iterate through the list of retrieved tournaments
            self.add_tournament_widget(tournament)  # Create and add a widget for each tournament


    def add_tournament_widget(self, tournament: dict) -> None:
        """
        **Creates and adds a tournament entry to the UI with a 'View Bracket' button.**
        
        **Why This Function Exists:**
        - Each tournament needs a distinct UI representation for users to interact with.
        - Displays tournament details retrieved dynamically from the database.
        - Provides a button that allows users to open the tournament bracket view.
        
        **Implementation Decisions:**
        - A `QFrame` is used to visually group each tournament's information.
        - A vertical layout (`QVBoxLayout`) ensures that elements are stacked properly.
        - A 'View Bracket' button is added for users to access the tournament details.
        - Lambda function is used in `clicked.connect()` to pass tournament data.
        
        **Parameters:**
        - `tournament` (dict): A dictionary containing tournament details retrieved from the database.
            - `"name"` (str): The name of the tournament.
        
        **Returns:**
        - None. This function modifies the UI by adding a new tournament widget.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Create a UI Container**
           - A `QFrame` is used to group the tournament's elements.
        
        2️⃣ **Step 2 - Add Tournament Title**
           - A `QLabel` is created and styled to display the tournament's name.
        
        3️⃣ **Step 3 - Create 'View Bracket' Button**
           - A button is added to allow users to open the bracket view.
           - The button is connected to `view_bracket()` to open the appropriate tournament details.
        
        4️⃣ **Step 4 - Add UI Components to Layout**
           - The tournament title and button are added to a vertical layout.
        
        5️⃣ **Step 5 - Add the Tournament Widget to the Main Layout**
           - The finalized `QFrame` is added to the main tournament layout.
        """
        
        # Step 1 - Create a UI Container
        container = QFrame()  # Creates a bordered frame to hold tournament details
        container.setStyleSheet(
            "background-color: #201212; border: 2px solid #8b0000; border-radius: 10px; padding: 10px;"
        )
        
        # Step 2 - Add Tournament Title
        container_layout = QVBoxLayout()  # Creates a vertical layout for stacking elements
        title_label = QLabel(tournament["name"])  # Retrieves and displays the tournament name
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ff5555;")
        container_layout.addWidget(title_label)  # Adds the title label to the layout
        
        # Step 3 - Create 'View Bracket' Button
        bracket_button = QPushButton("View Bracket")  # Button allowing users to view the tournament bracket
        bracket_button.setStyleSheet(
            "background-color: #ff5555; color: white; padding: 5px; border-radius: 5px;"
        )
        bracket_button.clicked.connect(lambda: self.view_bracket(tournament))  # Connect button to function
        container_layout.addWidget(bracket_button, alignment=Qt.AlignmentFlag.AlignCenter)  # Center-align the button
        
        # Step 4 - Set Layout to Container
        container.setLayout(container_layout)  # Apply layout to the tournament frame
        
        # Step 5 - Add the Tournament Widget to the Main Layout
        self.tournament_layout.addWidget(container)  # Add the entire tournament widget to the main layout

    def view_bracket(self, tournament_dict: dict) -> None:
        """
        **Opens the tournament bracket window for a selected tournament.**
        
        **Why This Function Exists:**
        - Tournament data is stored in a database and retrieved dynamically as a dictionary.
        - This function converts the dictionary into the appropriate tournament class instance.
        - Each tournament must be instantiated as an object to:
          - Manage tournament-specific data.
          - Track match progress dynamically.
          - Provide methods to update match results and standings.
        
        **Implementation Decisions:**
        - The function takes in a dictionary because tournaments are fetched dynamically from storage.
        - The `-> None` annotation is used because this function does not return a value; it only creates and opens a window.
        - Conditional checks determine which subclass should be instantiated to match the tournament type.
        - If the tournament type is invalid, an error message is printed for debugging purposes.
        
        **Parameters:**
        - `tournament_dict` (dict): A dictionary containing tournament details, including:
            - `"name"` (str): The tournament's name.
            - `"type"` (str): The tournament format (single_elimination, double_elimination, round_robin).
            - `"max_players"` (int): The maximum number of participants allowed.
        
        **Returns:**
        - None. This function does not return a value but instead opens a new window displaying the tournament bracket.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Extract Tournament Details**
           - Retrieve the tournament's `name`, `type`, and `max_players` from the dictionary.
           - Convert `max_players` to an integer to ensure it is in the correct format.
        
        2️⃣ **Step 2 - Validate Tournament Type and Create Instance**
           - Check the tournament type and instantiate the corresponding tournament class.
        
        3️⃣ **Step 3 - Handle Invalid Tournament Type**
           - If the tournament type is invalid, print an error message and exit.
        
        4️⃣ **Step 4 - Open the Tournament Bracket Window**
           - Pass the newly created tournament instance to `TournamentBracketDisplay`.
           - Open the tournament bracket window to display the bracket details.
        """
        
        # Step 1 - Extract Tournament Details
        tournament_name = tournament_dict["name"]  # Extracts the tournament's name
        tournament_type = tournament_dict["type"]  # Identifies the tournament format (single/double/round-robin)
        max_players = int(tournament_dict["max_players"])  # Ensures `max_players` is stored as an integer

        # Step 2 - Validate Tournament Type and Create Instance
        if tournament_type == "single_elimination":
            tournament_instance = SingleEliminationTournament(tournament_name, max_players)
        elif tournament_type == "double_elimination":
            tournament_instance = DoubleEliminationTournament(tournament_name, max_players)
        elif tournament_type == "round_robin":
            tournament_instance = RoundRobinTournament(tournament_name, max_players)
        
        # Step 3 - Handle Invalid Tournament Type
        else:
            print(f"❌ Error: Invalid tournament type '{tournament_type}'")  # Print error for debugging
            return  # Exit function to avoid processing an invalid tournament

        # Step 4 - Open the Tournament Bracket Window
        self.bracket_window = TournamentBracketDisplay(tournament_instance)  # Instantiate bracket display
        self.bracket_window.show()  # Open the tournament bracket window

class TournamentBracketDisplay(QWidget):
    """
    **Class Purpose:**
    - Displays the tournament bracket for an active tournament.
    - Dynamically generates and formats the bracket layout based on the tournament type.
    - Provides an interactive display where users can view matchups.
    
    **Why This Class Exists:**
    - Each tournament type (single elimination, double elimination, round robin) has a different bracket structure.
    - The display needs to be dynamically created based on tournament data.
    - Users should be able to visually follow tournament progress.
    
    **Implementation Decisions:**
    - Uses a `QVBoxLayout` to organize the tournament bracket visually.
    - Includes a scroll area to accommodate large brackets.
    - Calls the appropriate function based on the tournament type.
    """
    
    def __init__(self, tournament):
        """
        **Initializes the bracket display window.**
        **Parameters:**
        - `tournament` (Tournament): An instance of the selected tournament, containing match data.
        """
        super().__init__()
        
        # Validate Tournament Instance
        if isinstance(tournament, dict):
            print("❌ Error: Expected a Tournament instance but received a dictionary!")
            return  # Prevent further execution if incorrect data type is received
        
        # Configure Window
        self.tournament = tournament  # Store the tournament instance
        self.setWindowTitle(f"{tournament.name} - Bracket")  # Set the window title dynamically
        self.setGeometry(200, 200, 700, 500)  # Set window size
        
        # Create Main Layout
        main_layout = QVBoxLayout()
        
        # Add Tournament Title
        title = QLabel(f"{tournament.name} - Bracket")  # Create a title label
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")  # Style the title
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the title
        main_layout.addWidget(title)  # Add title to layout
        
        # Add Scroll Area
        scroll_area = QScrollArea(self)  # Create a scroll area for large brackets
        scroll_area.setWidgetResizable(True)  # Allow resizing to fit content
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Enable scroll bar if needed
        container = QWidget()  # Create a container for the bracket layout
        self.layout = QVBoxLayout(container)  # Use vertical layout inside the scroll area
        scroll_area.setWidget(container)  # Attach container to scroll area
        main_layout.addWidget(scroll_area)  # Add scroll area to main layout
        
        # Generate the Tournament Bracket
        # Determine the tournament type and generate the correct bracket
        if isinstance(self.tournament, RoundRobinTournament):
            self.create_round_robin_bracket(self.tournament)
        elif isinstance(self.tournament, SingleEliminationTournament):
            self.create_single_elimination_bracket(self.tournament)
        elif isinstance(self.tournament, DoubleEliminationTournament):
            self.create_double_elimination_bracket(self.tournament)
        
        # Add Close Button
        close_button = QPushButton("Close")  # Create a close button
        close_button.clicked.connect(self.close)  # Connect button to close the window
        main_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)  # Add button to layout
        
        # Set the final layout to the window
        self.setLayout(main_layout)


    def create_round_robin_bracket(self, tournament):
        """
        **Displays a round-robin tournament bracket using rounds from the Tournament instance.**
        
        **Why This Function Exists:**
        - Round-robin tournaments require a structured display to show all matchups.
        - Tournament rounds must be generated dynamically based on the number of players.
        - The match table must be visually formatted for clarity.
        
        **Implementation Decisions:**
        - Calls `generate_rounds()` to ensure matchups are created before display.
        - Uses a `QTableWidget` for structured data presentation.
        - Applies different styling to improve readability.
        
        **Parameters:**
        - `tournament` (RoundRobinTournament): The tournament instance containing match data.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Generate Tournament Rounds**
           - Calls `generate_rounds()` to create matchups.
        
        2️⃣ **Step 2 - Check if Rounds Exist**
           - If no rounds were generated, exit early to avoid errors.
        
        3️⃣ **Step 3 - Iterate Over Each Round**
           - Create a visual representation for each round.
           - `enumerate()` is used to automatically generate the round number while iterating. (enumerate is used for iterating in pairs)
           - This ensures each round is properly labeled without manually tracking the index.
        
        4️⃣ **Step 4 - Create and Style Round Labels**
           - Adds a label to indicate the current round number.
        
        5️⃣ **Step 5 - Create the Match Table**
           - Generates a `QTableWidget` to structure the match data.
        
        6️⃣ **Step 6 - Populate Match Table**
           - Inserts player names and table numbers into the table.
        
        7️⃣ **Step 7 - Update and Display Table**
           - Ensures the UI updates correctly and adds the table to the layout.
        """
        
        # Step 1 - Generate Tournament Rounds
        print(f"Generating rounds for tournament: {tournament.name}, Max Players: {tournament.max_players}")  # Debugging
        tournament.generate_rounds()  # Generate the rounds for the tournament
        print(f"Rounds generated: {tournament.rounds}")  # Debugging output displays number of rounds
        
        # Step 2 - Check if Rounds Exist
        if not tournament.rounds:
            print("No rounds were generated. Ensure max_players is set correctly.")
            return  # Exit if no rounds were created
        
        # Step 3 - Iterate Over Each Round and Matchup
        for round_number, matchups in enumerate(tournament.rounds, start=1):
            print(f"Round {round_number}: {matchups}")  # Debugging output
            
            # Step 4 - Create and Style Round Labels
            round_label = QLabel(f"🛡️ Round {round_number}")  # Create label
            round_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px; color: #ffcc00;")  # Style label
            round_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align label
            self.layout.addWidget(round_label)  # Add label to layout
            
            # Step 5 - Create the Round Table
            table = QTableWidget()  # Create table
            table.setColumnCount(4)  # Define number of columns
            table.setRowCount(len(matchups))  # Set number of rows to match number of matchups
            
            # Set Headers for the Table
            headers = ["Player 1", "Player 2", "Winner", "Table Number"]  # Column headers
            for col, header_text in enumerate(headers):  # Assign headers to table
                table.setHorizontalHeaderItem(col, QTableWidgetItem(header_text))
            
            # Step 6 - Style and Populate Match Table
            table.horizontalHeader().setVisible(True)  # Show headers
            table.verticalHeader().setVisible(False)  # Hide vertical headers
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            
            for row, match in enumerate(matchups):
                table.setItem(row, 0, QTableWidgetItem(match["p1"]))  # Player 1
                table.setItem(row, 1, QTableWidgetItem(match["p2"]))  # Player 2
                table.setItem(row, 3, QTableWidgetItem(str(match["table"])))  # Table Number
            
            # Step 7 - Update and Display Table
            table.viewport().update()  # Force UI refresh (otherwise the table will not show)
            self.layout.addWidget(table)  # Add table to layout

    def create_single_elimination_bracket(self, tournament):
        """
        **Displays a single elimination tournament bracket using rounds from the Tournament instance.**
        
        **Why This Function Exists:**
        - Single elimination tournaments require a structured bracket display.
        - Tournament rounds must be dynamically generated based on the number of players.
        - The match table must be visually formatted for clarity.
        
        **Implementation Decisions:**
        - Calls `generate_rounds()` to ensure matchups are created before display.
        - Uses a `QTableWidget` for structured data presentation.
        - Applies different styling to improve readability.
        
        **Parameters:**
        - `tournament` (SingleEliminationTournament): The tournament instance containing match data.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Generate Tournament Rounds**
           - Calls `generate_rounds()` to create matchups.
        
        2️⃣ **Step 2 - Check if Rounds Exist**
           - If no rounds were generated, exit early to avoid errors.
        
        3️⃣ **Step 3 - Iterate Over Each Round**
           - Create a visual representation for each round.
           - `enumerate()` is used to automatically generate the round number while iterating. (enumerate is used for iterating in pairs)
           - This ensures each round is properly labeled without manually tracking the index.
        
        4️⃣ **Step 4 - Create and Style Round Labels**
           - Adds a label to indicate the current round number.
        
        5️⃣ **Step 5 - Create the Match Table**
           - Generates a `QTableWidget` to structure the match data.
        
        6️⃣ **Step 6 - Populate Match Table**
           - Inserts player names and table numbers into the table.
        
        7️⃣ **Step 7 - Update and Display Table**
           - Ensures the UI updates correctly and adds the table to the layout.
        """
        
        # Step 1 - Generate Tournament Rounds
        print(f"Generating rounds for tournament: {tournament.name}, Max Players: {tournament.max_players}")  # Debugging
        tournament.generate_rounds()  # Generate the rounds for the tournament
        print(f"Rounds generated: {tournament.rounds}")  # Debugging output displays number of rounds
        
        # Step 2 - Check if Rounds Exist
        if not tournament.rounds:
            print("No rounds were generated. Ensure max_players is set correctly.")
            return  # Exit if no rounds were created
        
        # Step 3 - Iterate Over Each Round and Matchup
        for round_number, matchups in enumerate(tournament.rounds, start=1):
            print(f"Round {round_number}: {matchups}")  # Debugging output
            
            # Step 4 - Create and Style Round Labels
            round_label = QLabel(f"🛡️ Round {round_number}")  # Create label
            round_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px; color: #ffcc00;")  # Style label
            round_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align label
            self.layout.addWidget(round_label)  # Add label to layout
            
            # Step 5 - Create the Round Table
            table = QTableWidget()  # Create table
            table.setColumnCount(4)  # Define number of columns
            table.setRowCount(len(matchups))  # Set number of rows to match number of matchups
            
            # Set Headers for the Table
            headers = ["Player 1", "Player 2", "Winner", "Table Number"]  # Column headers
            for col, header_text in enumerate(headers):  # Assign headers to table
                table.setHorizontalHeaderItem(col, QTableWidgetItem(header_text))
            
            # Step 6 - Style and Populate Match Table
            table.horizontalHeader().setVisible(True)  # Show headers
            table.verticalHeader().setVisible(False)  # Hide vertical headers
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            
            for row, match in enumerate(matchups):
                table.setItem(row, 0, QTableWidgetItem(match["p1"]))  # Player 1
                table.setItem(row, 1, QTableWidgetItem(match["p2"]))  # Player 2
                # The table number is omitted to avoid a runtime error
            
            # Step 7 - Update and Display Table
            table.viewport().update()  # Force UI refresh (otherwise the table will not show)
            self.layout.addWidget(table)  # Add table to layout

    def create_double_elimination_bracket(self, tournament):
        """
        **Displays a double elimination tournament bracket using rounds from the Tournament instance.**
        
        **Why This Function Exists:**
        - Double elimination tournaments require a structured bracket display.
        - Tournament rounds must be dynamically generated based on the number of players.
        - Players are only eliminated after two losses, making future matchups more complex.
        
        **Implementation Decisions:**
        - Calls `generate_rounds()` to ensure matchups are created before display.
        - Uses a `QTableWidget` for structured data presentation.
        - Applies different styling to improve readability.
        
        **Parameters:**
        - `tournament` (DoubleEliminationTournament): The tournament instance containing match data.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Generate Tournament Rounds**
           - Calls `generate_rounds()` to create matchups.
        
        2️⃣ **Step 2 - Check if Rounds Exist**
           - If no rounds were generated, exit early to avoid errors.
        
        3️⃣ **Step 3 - Iterate Over Each Round**
           - Create a visual representation for each round.
           - `enumerate()` is used to automatically generate the round number while iterating. (enumerate is used for iterating in pairs)
           - This ensures each round is properly labeled without manually tracking the index.
        
        4️⃣ **Step 4 - Create and Style Round Labels**
           - Adds a label to indicate the current round number.
        
        5️⃣ **Step 5 - Create the Match Table**
           - Generates a `QTableWidget` to structure the match data.
        
        6️⃣ **Step 6 - Populate Match Table**
           - Inserts player names and determines the winner based on match results.
        
        7️⃣ **Step 7 - Update and Display Table**
           - Ensures the UI updates correctly and adds the table to the layout.
        """
        
        # Step 1 - Generate Tournament Rounds
        print(f"Generating rounds for tournament: {tournament.name}, Max Players: {tournament.max_players}")  # Debugging
        tournament.generate_rounds()  # Generate the rounds for the tournament
        print(f"Rounds generated: {tournament.rounds}")  # Debugging output displays number of rounds
        
        # Step 2 - Check if Rounds Exist
        if not tournament.rounds:
            print("❌ No rounds were generated. Ensure max_players is set correctly.")
            return  # Exit if no rounds were created
        
        # Step 3 - Iterate Over Each Round and Matchup
        for round_number, matchups in enumerate(tournament.rounds, start=1):
            print(f"Round {round_number}: {matchups}")  # Debugging output
            
            # Step 4 - Create and Style Round Labels
            round_label = QLabel(f"🛡️ Round {round_number}")  # Create label
            round_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px; color: #ffcc00;")  # Style label
            round_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align label
            self.layout.addWidget(round_label)  # Add label to layout
            
            # Step 5 - Create the Round Table
            table = QTableWidget()  # Create table
            table.setColumnCount(3)  # Define number of columns
            table.setRowCount(len(matchups))  # Set number of rows to match number of matchups
            
            # Set Headers for the Table
            headers = ["Player 1", "Player 2", "Winner"]  # Column headers
            for col, header_text in enumerate(headers):  # Assign headers to table
                table.setHorizontalHeaderItem(col, QTableWidgetItem(header_text))
            
            # Step 6 - Style and Populate Match Table
            table.horizontalHeader().setVisible(True)  # Show headers
            table.verticalHeader().setVisible(False)  # Hide vertical headers
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            
            for row, match in enumerate(matchups):
                if isinstance(match, dict):  # Ensure the match is in dictionary format
                    player1 = str(match.get("p1", "TBD"))  # Get player 1's name or TBD if unknown
                    player2 = str(match.get("p2", "TBD"))  # Get player 2's name or TBD if unknown
                    winner = str(match.get("winner", "TBD"))  # Get the winner or TBD if undecided
                    
                    table.setItem(row, 0, QTableWidgetItem(player1))  # Set Player 1
                    table.setItem(row, 1, QTableWidgetItem(player2))  # Set Player 2
                    table.setItem(row, 2, QTableWidgetItem(winner))  # Set Winner
                else:
                    print(f"❌ Unexpected match format: {match}")  # Debugging
            
            # Step 7 - Update and Display Table
            table.viewport().update()  # Force UI refresh (otherwise the table will not show)
            self.layout.addWidget(table)  # Add table to layout


# Saved code for winner button to be added into each bracket table
# Would be added at the end of step 6 as part of populating the table
"""
# Create a button group so only one can be selected
winner_group = QButtonGroup(table)

# Radio buttons for each player
p1_button = QRadioButton(match["p1"])
p2_button = QRadioButton(match["p2"])

# Add them to the button group (so only one can be selected at a time)
winner_group.addButton(p1_button)
winner_group.addButton(p2_button)

# Connect selection to set_winner method
p1_button.toggled.connect(lambda checked, r=round_number, m=match, p=match["p1"]: self.tournament.set_winner(r, m, p) if checked else None)
p2_button.toggled.connect(lambda checked, r=round_number, m=match, p=match["p2"]: self.tournament.set_winner(r, m, p) if checked else None)

# Add to the table
table.setCellWidget(row, 2, p1_button)
table.setCellWidget(row, 3, p2_button)
"""