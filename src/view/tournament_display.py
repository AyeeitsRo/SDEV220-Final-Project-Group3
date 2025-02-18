from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, 
    QTableWidgetItem, QFrame
)
from PyQt6.QtCore import Qt
from model.current_events import CurrentEvents

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
        self.events = CurrentEvents()

        if not self.events.tournaments:
            no_tournaments = QLabel("No tournaments currently available.")
            no_tournaments.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_tournaments.setStyleSheet("font-size: 16px; color: gray;")
            self.tournament_layout.addWidget(no_tournaments)
            return

        for game, tournaments in self.events.tournaments.items():
            for tournament in tournaments:
                self.add_tournament_widget(game, tournament)

    def add_tournament_widget(self, game, tournament):
        """Adds a tournament entry with a 'View Bracket' button."""
        container = QFrame()
        container.setStyleSheet("background-color: #201212; border: 2px solid #8b0000; border-radius: 10px; padding: 10px;")
        container_layout = QVBoxLayout()

        title_label = QLabel(tournament["name"])
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ff5555;")
        container_layout.addWidget(title_label)

        bracket_button = QPushButton("View Bracket")
        bracket_button.setStyleSheet("background-color: #ff5555; color: white; padding: 5px; border-radius: 5px;")
        bracket_button.clicked.connect(lambda: self.view_bracket(game, tournament))
        container_layout.addWidget(bracket_button, alignment=Qt.AlignmentFlag.AlignCenter)

        container.setLayout(container_layout)
        self.tournament_layout.addWidget(container)

    def view_bracket(self, game, tournament):
        """Opens the tournament bracket window."""
        self.bracket_window = TournamentBracketDisplay(self, game, tournament)
        self.bracket_window.show()


class TournamentBracketDisplay(QWidget):
    def __init__(self, parent, game, tournament):
        """Displays the tournament bracket."""
        super().__init__()
        self.parent = parent
        self.setWindowTitle(f"{tournament['name']} - Bracket")
        self.setGeometry(200, 200, 700, 500)

        self.layout = QVBoxLayout()

        title = QLabel(f"{tournament['name']} - Bracket")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title)

        # Generate bracket for Round Robin
        if tournament.get("type") == "round_robin":
            self.create_round_robin_bracket(tournament)
        
        # Generate bracket for Single Elimination

        # Generate bracket for Double Elimination

        # Generate bracket for Swiss System

        # Add Close button to return to tournament display
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        self.layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

    def create_round_robin_bracket(self, tournament):
        """Creates a round-robin tournament bracket."""
        players = tournament.get("players", ["Player 1", "Player 2", "Player 3", "Player 4"])
        rounds = [
            [("Player 1", "Player 4"), ("Player 2", "Player 3")],
            [("Player 1", "Player 3"), ("Player 4", "Player 2")],
            [("Player 1", "Player 2"), ("Player 3", "Player 4")]
        ]

        for round_number, matchups in enumerate(rounds, start=1):
            round_label = QLabel(f"Round {round_number}")
            round_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
            self.layout.addWidget(round_label)

            table = QTableWidget()
            table.setColumnCount(4)
            headers:list = ["Player 1", "Player 2", "Winner", "Table Number"]
            table.setHorizontalHeaderLabels(headers)
            table.horizontalHeader().setVisible(True)
            table.setRowCount(len(matchups))

            table.setStyleSheet("""
                border: 2px solid #8b0000;
                background-color: #201212;
                color: white;
                padding: 5px;
            """)

            for row, (player1, player2) in enumerate(matchups):
                table.setItem(row, 0, QTableWidgetItem(player1))
                table.setItem(row, 1, QTableWidgetItem(player2))
                # Admin view button for functional and testing purposes
                winner_button = QPushButton("Set Winner")
                winner_button.setStyleSheet("background-color: #ff5555; color: white; border-radius: 5px; padding: 5px")
                # Styling of button above is due to css style sheet not reaching buttons in a loop
                table.setCellWidget(row, 2, winner_button)

                table.setItem(row, 3, QTableWidgetItem(str(row + 1)))  # Table Number

            self.layout.addWidget(table)

