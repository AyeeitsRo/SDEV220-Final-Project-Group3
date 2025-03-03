from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, 
    QTableWidgetItem, QFrame, QHeaderView, QScrollArea
)
from PyQt6.QtCore import Qt
from model.current_events import CurrentEvents
from model.tournament import *

class TournamentDisplay(QWidget):
    def __init__(self, controller):
        """Initializes the TournamentDisplay window."""
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Tournaments")
        self.setGeometry(100, 100, 900, 650)
        
        self.tournament_layout = QVBoxLayout()

        # Header Section
        top_container = QHBoxLayout()
        header_label = QLabel("Tournaments")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        top_container.addWidget(header_label, 3)
        top_container.addWidget(close_button, 1)
        self.tournament_layout.addLayout(top_container)

        # Load tournaments from current events
        self.load_tournaments()

        self.setLayout(self.tournament_layout)

    def load_tournaments(self):
        """Loads and displays active tournaments."""
        # Create instance
        self.events = CurrentEvents()
        # Get all of the tournaments
        all_tournaments = self.events.get_all_tournaments()

        if not all_tournaments:
            no_tournaments = QLabel("No tournaments currently available.")
            no_tournaments.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_tournaments.setStyleSheet("font-size: 16px; color: gray;")
            self.tournament_layout.addWidget(no_tournaments)
            return

        for tournament in all_tournaments:
                self.add_tournament_widget(tournament)

    def add_tournament_widget(self, tournament):
        """Adds a tournament entry with a 'View Bracket' button."""
        container = QFrame()
        container.setStyleSheet("background-color: #201212; border: 2px solid #8b0000; border-radius: 10px; padding: 10px;")
        container_layout = QVBoxLayout()

        title_label = QLabel(tournament["name"])
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ff5555;")
        container_layout.addWidget(title_label)

        bracket_button = QPushButton("View Bracket")
        bracket_button.setStyleSheet("background-color: #ff5555; color: white; padding: 5px; border-radius: 5px;")
        bracket_button.clicked.connect(lambda: self.view_bracket(tournament))
        container_layout.addWidget(bracket_button, alignment=Qt.AlignmentFlag.AlignCenter)

        container.setLayout(container_layout)
        self.tournament_layout.addWidget(container)

    def view_bracket(self, tournament):
        """Opens the tournament bracket window."""
        max_players = tournament["max_players"]
        self.bracket_window = TournamentBracketDisplay(self, tournament)
        self.bracket_window.show()


class TournamentBracketDisplay(QWidget):
    def __init__(self, parent, tournament):
        """Displays the tournament bracket."""
        super().__init__()
        self.parent = parent
        self.setWindowTitle(f"{tournament['name']} - Bracket")
        self.setGeometry(200, 200, 700, 500)

        main_layout = QVBoxLayout()

        title = QLabel(f"{tournament['name']} - Bracket")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Scroll Area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        container = QWidget()
        self.layout = QVBoxLayout(container)

        # Generate bracket for tournaments
        tournament_type = tournament.get("type")
        max_players = tournament.get("max_players")

        if tournament_type == "round_robin":
            tournament_instance = RoundRobinTournament(tournament['name'], int(max_players))
            self.create_round_robin_bracket(tournament_instance)
        elif tournament_type == "single_elimination":
            tournament_instance = SingleEliminationTournament(tournament['name'], int(max_players))
            self.create_single_elimination_bracket(tournament_instance)
        elif tournament_type == "double_elimination":
            tournament_instance = DoubleEliminationTournament(tournament['name'], int(max_players))
            self.create_double_elimination_bracket(tournament_instance)

        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)
        # Add Close button to return to tournament display
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)

    def create_round_robin_bracket(self, tournament):
        """Displays a round-robin tournament bracket using rounds from the Tournament instance."""

        print(f"Generating rounds for tournament: {tournament.name}, Max Players: {tournament.max_players}") # Debugging
        tournament.generate_rounds()
        print(f"Rounds generated: {tournament.rounds}")  # Debugging
        
        if not tournament.rounds:
            print("No rounds were generated. Ensure max_players is set correctly.")
            return

        for round_number, matchups in enumerate(tournament.rounds, start=1):
            print(f"Round {round_number}: {matchups}")  # Debugging
            round_label = QLabel(f"🛡️ Round {round_number}")
            round_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px; color: #ffcc00;")
            round_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(round_label)

            table = QTableWidget()
            table.setColumnCount(4)
            table.setRowCount(len(matchups))

            # Set Headers
            headers = ["Player 1", "Player 2", "Winner", "Table Number"]
            for col, header_text in enumerate(headers):
                table.setHorizontalHeaderItem(col, QTableWidgetItem(header_text))

            # Header Visibility
            table.horizontalHeader().setVisible(True)
            table.verticalHeader().setVisible(False)

            # Header Sizing
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

            for row, match in enumerate(matchups):
                table.setItem(row, 0, QTableWidgetItem(match["p1"]))
                table.setItem(row, 1, QTableWidgetItem(match["p2"]))
                table.setItem(row, 3, QTableWidgetItem(str(match["table"])))

                # Winner Button
                winner_button = QPushButton("Set Winner")
                winner_button.setStyleSheet("""
                    background-color: #ff5555;
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                    border-radius: 5px;
                    padding: 1px, 1px;
                    min-height: 15px;
                """)
                table.setCellWidget(row, 2, winner_button)

            # Force UI Update
            table.viewport().update()
            self.layout.addWidget(table)


    def create_single_elimination_bracket(self, tournament):
        print(f"Generating rounds for tournament: {tournament.name}, Max Players: {tournament.max_players}") # Debugging
        tournament.generate_rounds()
        print(f"Rounds generated: {tournament.rounds}")  # Debugging
        
        if not tournament.rounds:
            print("No rounds were generated. Ensure max_players is set correctly.")
            return

        for round_number, matchups in enumerate(tournament.rounds, start=1):
            print(f"Round {round_number}: {matchups}")  # Debugging
            round_label = QLabel(f"🛡️Round {round_number}")
            round_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px; color: #ffcc00;")
            round_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(round_label)

            table = QTableWidget()
            table.setColumnCount(4)
            table.setRowCount(len(matchups))

            # Set Headers
            headers = ["Player 1", "Player 2", "Winner", "Table Number"]
            for col, header_text in enumerate(headers):
                table.setHorizontalHeaderItem(col, QTableWidgetItem(header_text))

            # Header Visibility
            table.horizontalHeader().setVisible(True)
            table.verticalHeader().setVisible(False)

            # Header Sizing
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

            for row, match in enumerate(matchups):
                table.setItem(row, 0, QTableWidgetItem(match["p1"]))
                table.setItem(row, 1, QTableWidgetItem(match["p2"]))

                # Winner Button
                winner_button = QPushButton("Set Winner")
                winner_button.setStyleSheet("""
                    background-color: #ff5555;
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                    border-radius: 5px;
                    padding: 1px, 1px;
                    min-height: 15px;
                """)
                table.setCellWidget(row, 2, winner_button)

            # Force UI Update
            table.viewport().update()
            self.layout.addWidget(table)

    def create_double_elimination_bracket(self, tournament):
        print(f"Generating rounds for tournament: {tournament.name}, Max Players: {tournament.max_players}")  # Debugging
        tournament.generate_rounds()  # Ensure rounds are generated
        print(f"Rounds generated: {tournament.rounds}")  # Debugging

        if not tournament.rounds:
            print("❌ No rounds were generated. Ensure max_players is set correctly.")
            return

        # Iterate through rounds (each round will be displayed separately)
        for round_number, round_info in enumerate(tournament.rounds, start=1):
            print(f"Round {round_number}: {round_info['matches']}")  # Debugging

            # Section Label for the Round
            round_label = QLabel(f"🛡️ Round {round_number}")
            round_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px; color: #ffcc00;")
            round_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(round_label)

            # Create Table
            table = QTableWidget()
            table.setColumnCount(3)  # Player 1, Player 2, Winner
            table.setRowCount(len(round_info["matches"]))

            # Set Headers
            headers = ["Player 1", "Player 2", "Winner"]
            for col, header_text in enumerate(headers):
                table.setHorizontalHeaderItem(col, QTableWidgetItem(header_text))

            # Show Headers for Better Clarity
            table.horizontalHeader().setVisible(True)
            table.verticalHeader().setVisible(True)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            # Populate Table with Matches
            for row, match in enumerate(round_info["matches"]):
                if isinstance(match, dict):
                    player1 = str(match.get("p1", "TBD"))
                    player2 = str(match.get("p2", "TBD"))
                    winner = str(match.get("winner", "TBD"))

                    table.setItem(row, 0, QTableWidgetItem(player1))
                    table.setItem(row, 1, QTableWidgetItem(player2))
                    table.setItem(row, 2, QTableWidgetItem(winner))

                    # Add a Winner Button for Manual Winner Entry
                    winner_button = QPushButton("Set Winner")
                    winner_button.setStyleSheet("""
                        background-color: #ff5555;
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                        border-radius: 5px;
                        padding: 1px, 1px;
                        min-height: 15px;
                    """)
                    table.setCellWidget(row, 2, winner_button)
                else:
                    print(f"❌ Unexpected match format: {match}")  # Debugging

            # Add Table to Layout
            table.viewport().update()
            self.layout.addWidget(table)

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

