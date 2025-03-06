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
    def __init__(self, tournament):
        """Displays the tournament bracket."""
        super().__init__()

        # Make sure the tournament data was sent as an instance and not as a dictionary
        if isinstance(tournament, dict):
            print("❌ Error: Expected a Tournament instance but received a dictionary!")
            return
        
        # Create Window for bracket
        self.tournament = tournament
        self.setWindowTitle(f"{tournament.name} - Bracket")
        self.setGeometry(200, 200, 700, 500)

        # Main layout
        main_layout = QVBoxLayout()

        # Title in main layout, which will be the name of the tournament
        title = QLabel(f"{tournament.name} - Bracket")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Scroll Area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        container = QWidget()
        self.layout = QVBoxLayout(container)

        # Add the scroll area to the container and main layout
        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

        # Check that the data from each tournament-type class is also an instance
        # Send to the appropriate bracket function according to the type of tournament
        if isinstance(self.tournament, RoundRobinTournament):
            self.create_round_robin_bracket(self.tournament)
        elif isinstance(self.tournament, SingleEliminationTournament):
            self.create_single_elimination_bracket(self.tournament)
        elif isinstance(self.tournament, DoubleEliminationTournament):
            self.create_double_elimination_bracket(self.tournament)

        # Add Close button to return to tournament display
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set the main layout to the window
        self.setLayout(main_layout)

    def create_round_robin_bracket(self, tournament):
        """Displays a round-robin tournament bracket using rounds from the Tournament instance."""

        # Debugging tools below help to check that the data for the tournament was successfully obtained and passed
        print(f"Generating rounds for tournament: {tournament.name}, Max Players: {tournament.max_players}") # Debugging
        # Call to the generate rounds function to add all the necessary rounds for the tournament
        tournament.generate_rounds()
        print(f"Rounds generated: {tournament.rounds}")  # Debugging
        
        # If no rounds were generated, this decision statement is ran
        if not tournament.rounds:
            print("No rounds were generated. Ensure max_players is set correctly.")
            return

        # Iterate through each pair of objects: round number and matchups (the players assigned to compete), for each round
        # Create a label to display the data for each iteration
        for round_number, matchups in enumerate(tournament.rounds, start=1):
            print(f"Round {round_number}: {matchups}")  # Debugging, shows the round number and players that were passed
            # Create the label for the round number
            round_label = QLabel(f"🛡️ Round {round_number}")
            round_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px; color: #ffcc00;")
            round_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(round_label)
            # Create a table for the round
            table = QTableWidget()
            table.setColumnCount(4)
            table.setRowCount(len(matchups)) # The number of rows are dependant on the number of matchups there are in a round

            # Set Headers for the table
            headers = ["Player 1", "Player 2", "Winner", "Table Number"] 
            # Iterate through the pairs col (column number) and header_text and pass the headers list through to be assigned as a header in the table
            for col, header_text in enumerate(headers):
                table.setHorizontalHeaderItem(col, QTableWidgetItem(header_text))

            # Set the Header Visibility
            table.horizontalHeader().setVisible(True)
            table.verticalHeader().setVisible(False)

            # Set the Header Sizing
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

            # Iterate through the pairs row (row number) and match, and pass through each matchup (the players competing in that match/round)
            # Put each player and the assigned table number that they will sit at in the cafe into the table
            for row, match in enumerate(matchups):
                table.setItem(row, 0, QTableWidgetItem(match["p1"]))
                table.setItem(row, 1, QTableWidgetItem(match["p2"]))
                table.setItem(row, 3, QTableWidgetItem(str(match["table"])))
            """
                # Add a Winner Button for Manual Winner Entry
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

            # Force UI Update so that the headers will show in the table, otherwise they will not show
            table.viewport().update()
            # Add to the table
            self.layout.addWidget(table)


    def create_single_elimination_bracket(self, tournament):
        """ Displays a single elimination tournament bracket for any tournament listed as a single elimination """
        # Debugging below prints tournament data to ensure that the correct information was gathered.
        print(f"Generating rounds for tournament: {tournament.name}, Max Players: {tournament.max_players}") # Debugging
        # Call to the generate rounds function for this tournament
        tournament.generate_rounds()
        print(f"Rounds generated: {tournament.rounds}")  # Debugging shows the number of rounds that were created.
        
        # If no rounds are generated, this decision statement will run.
        if not tournament.rounds:
            print("No rounds were generated. Ensure max_players is set correctly.")
            return
        # Iterate through each pair of objects: round number and matchups (the players assigned to compete), for each round
        # Create a label to display the data for each iteration
        for round_number, matchups in enumerate(tournament.rounds, start=1):
            print(f"Round {round_number}: {matchups}")  # Debugging
            # Create the label for the round number
            round_label = QLabel(f"🛡️Round {round_number}")
            round_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px; color: #ffcc00;")
            round_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(round_label)
            # Create the table for the round
            table = QTableWidget()
            table.setColumnCount(4)
            table.setRowCount(len(matchups)) # Amount of rows is dependent on the number of matchups created for the round

            # Set Headers for the table
            headers = ["Player 1", "Player 2", "Winner", "Table Number"]
            # Iterate through the pairs col (column number) and header_text and pass the headers list through to be assigned as a header in the table
            for col, header_text in enumerate(headers):
                table.setHorizontalHeaderItem(col, QTableWidgetItem(header_text))

            # Set the Header Visibility
            table.horizontalHeader().setVisible(True)
            table.verticalHeader().setVisible(False)

            # Set the Header Sizing
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

            # Iterate through the pairs row (row number) and match, and pass through each matchup (the players competing in that match/round)
            # Put each player and the assigned table number that they will sit at in the cafe into the table
            for row, match in enumerate(matchups):
                table.setItem(row, 0, QTableWidgetItem(match["p1"]))
                table.setItem(row, 1, QTableWidgetItem(match["p2"]))
                # Do not put a table number here, for some reason it causes a run time error
            """
                # Add a Winner Button for Manual Winner Entry
                # Create a button group so only one can be selected
                winner_group = QButtonGroup(table)
    
                # Radio buttons for each player
                p1_button = QRadioButton(match["p1"])
                p2_button = QRadioButton(match["p2"])

                # Add them to the button group (so only one can be selected at a time)
                winner_group.addButton(p1_button)
                winner_group.addButton(p2_button)

                # Connect selection to set_winner method
                p1_button.toggled.connect(lambda checked: self.tournament.set_winner(round_number, match, match["p1"]) if checked else None)
                p2_button.toggled.connect(lambda checked: self.tournament.set_winner(round_number, match, match["p2"]) if checked else None)

                # Add to the table
                table.setCellWidget(row, 2, p1_button)
                table.setCellWidget(row, 3, p2_button)
            """

            # Force UI Update otherwise the headers for the table will not show
            table.viewport().update()
            # Add the table to the layout
            self.layout.addWidget(table)

    def create_double_elimination_bracket(self, tournament):
        """ Creates a bracket for any tournament type that is set as a double elimination tournament """
        # Debugging below displays tournament data to make sure the correct information is being obtained and passed through.
        print(f"Generating rounds for tournament: {tournament.name}, Max Players: {tournament.max_players}")  # Debugging
        # Call the function to generate rounds for this tournament
        tournament.generate_rounds() 
        print(f"Rounds generated: {tournament.rounds}")  # Debugging
        
        # If no rounds are generated, this decision statement will run
        if not tournament.rounds:
            print("❌ No rounds were generated. Ensure max_players is set correctly.")
            return

        # Iterate through each pair of objects: round number and matchups (the players assigned to compete), for each round
        # Create a label to display the data for each iteration
        for round_number, matchups in enumerate(tournament.rounds, start=1):
            print(f"Round {round_number}: {matchups}")  # Debugging

            # Create a label for the round number
            round_label = QLabel(f"🛡️ Round {round_number}")
            round_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px; color: #ffcc00;")
            round_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(round_label)

            # Create the table for the round
            table = QTableWidget()
            table.setColumnCount(3)
            table.setRowCount(len(matchups)) # The amount of rows is dependent on the number of matchups

            # Set Headers for the table
            headers = ["Player 1", "Player 2", "Winner"]

            # Iterate through the pairs col (column number) and header_text and pass the headers list through to be assigned as a header in the table
            for col, header_text in enumerate(headers):
                table.setHorizontalHeaderItem(col, QTableWidgetItem(header_text))

            # Set the visibility for the headers
            table.horizontalHeader().setVisible(True)
            table.verticalHeader().setVisible(True)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            # Iterate through the pairs row (row number) and match, and pass through each matchup (the players competing in that match/round)
            # Put each player and the assigned table number that they will sit at in the cafe into the table
            for row, match in enumerate(matchups):
                # Check that the matchup is an instance
                # In double elimination, future matchups are not able to be determined due to each player needing to lose twice in order to be eliminated
                # Therefore, each matchup needs to be an instance based on the players that have not been eliminated
                if isinstance(match, dict):
                    # Assign each player in the match instance with the gamertag, or with TBD
                    player1 = str(match.get("p1", "TBD"))
                    player2 = str(match.get("p2", "TBD"))
                    winner = str(match.get("winner", "TBD"))
                    # Add each into the table
                    table.setItem(row, 0, QTableWidgetItem(player1))
                    table.setItem(row, 1, QTableWidgetItem(player2))
                    table.setItem(row, 2, QTableWidgetItem(winner))
                """
                    # Add a Winner Button for Manual Winner Entry
                    # Create a button group so only one can be selected
                    winner_group = QButtonGroup(table)
    
                    # Radio buttons for each player
                    p1_button = QRadioButton(match["p1"])
                    p2_button = QRadioButton(match["p2"])

                    # Add them to the button group (so only one can be selected at a time)
                    winner_group.addButton(p1_button)
                    winner_group.addButton(p2_button)

                    # Connect selection to set_winner method
                    p1_button.toggled.connect(lambda checked: self.tournament.set_winner(round_number, match, match["p1"]) if checked else None)
                    p2_button.toggled.connect(lambda checked: self.tournament.set_winner(round_number, match, match["p2"]) if checked else None)

                    # Add to the table
                    table.setCellWidget(row, 2, p1_button)
                    table.setCellWidget(row, 3, p2_button)
                
                else:
                    print(f"❌ Unexpected match format: {match}")  # Debugging
                """
            # Add Table to Layout and for a UI update on the table
            table.viewport().update()
            self.layout.addWidget(table)


        """
        # **Grand Finals**
        if hasattr(tournament, "grand_finals"):
            final_label = QLabel("🏆 Grand Finals")
            final_label.setStyleSheet("font-size: 22px; font-weight: bold; margin-top: 20px; color: #ff0000;")
            final_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(final_label)

            final_table = QTableWidget()
            final_table.setColumnCount(3)
            final_table.setRowCount(1)
            final_table.setHorizontalHeaderItem(0, QTableWidgetItem("Player 1"))
            final_table.setHorizontalHeaderItem(1, QTableWidgetItem("Player 2"))
            final_table.setHorizontalHeaderItem(2, QTableWidgetItem("Winner"))

            final_table.setItem(0, 0, QTableWidgetItem(tournament.grand_finals["p1"]))
            final_table.setItem(0, 1, QTableWidgetItem(tournament.grand_finals["p2"]))
            final_table.setItem(0, 2, QTableWidgetItem(str(tournament.grand_finals["winner"])))

            self.layout.addWidget(final_table)

        """