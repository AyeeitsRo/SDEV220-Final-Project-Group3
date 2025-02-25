import math
import sqlite3

class Tournament:
    """Base tournament class for different formats."""

    def __init__(self, name, max_players):
        self.name = name
        self.max_players = max_players
        self.players = []  # List of gamer tags
        self.rounds = []  # Tournament bracket rounds
        self.create_initial_bracket()

    def create_initial_bracket(self):
        """Generates an empty bracket structure based on player count."""
        self.rounds = [[] for _ in range(self.get_round_count())]
        for i in range(self.max_players // 2):
            self.rounds[0].append(("Open Slot", "Open Slot"))

    def get_round_count(self):
        """Returns the number of rounds needed for a single-elimination tournament."""
        return math.ceil(math.log2(self.max_players))

    def add_player(self, gamer_tag):
        """Assigns a player to an open slot in the first round."""
        for i, (p1, p2) in enumerate(self.rounds[0]):
            if p1 == "Open Slot":
                self.rounds[0][i] = (gamer_tag, p2)
                return True
            elif p2 == "Open Slot":
                self.rounds[0][i] = (p1, gamer_tag)
                return True
        return False  # Tournament is full

    def get_bracket(self):
        """Returns the tournament bracket with matches per round."""
        return self.rounds

class SingleEliminationTournament(Tournament):
    """Single elimination format: lose once = eliminated."""

    def generate_bracket(self):
        """Generates matchups for a single-elimination bracket."""
        self.bracket = []
        num_matches = len(self.players) // 2
        for i in range(num_matches):
            self.bracket.append([self.players[i * 2], self.players[i * 2 + 1]])

        if len(self.players) % 2 != 0:
            self.bracket.append([self.players[-1], None])  # Last player advances automatically

class DoubleEliminationTournament(Tournament):
    """Double elimination format: Two losses before elimination."""

    def generate_bracket(self):
        """Generates an initial double-elimination bracket."""
        self.winners_bracket = []
        self.losers_bracket = []

        num_matches = len(self.players) // 2
        for i in range(num_matches):
            self.winners_bracket.append([self.players[i * 2], self.players[i * 2 + 1]])

        if len(self.players) % 2 != 0:
            self.winners_bracket.append([self.players[-1], None])  # Last player advances automatically

class RoundRobinTournament:
    def __init__(self, name, max_players):
        self.name = name
        self.max_players = max_players
        self.players = self.load_registered_players()  # Fetch registered players
        self.rounds = []

        print(f"Creating RoundRobinTournament: {self.name} with max_players: {self.max_players}")
        print(f"Initial players list: {self.players}")

        self.fill_empty_slots()  # Fill empty slots (Otherwise you get no table view of the brackets)
        self.generate_rounds() # Generates rounds based off of max players

    def load_registered_players(self):
        """Fetches players signed up for this tournament from the database."""
        conn = sqlite3.connect("src/game_cafe.db")
        cursor = conn.cursor()
        cursor.execute("SELECT gamertag FROM event_signup WHERE event_name = ?", (self.name,))
        players = [row[0] for row in cursor.fetchall()]
        conn.close()

        if not players:
            print(f"No registered players for {self.name}, initializing empty slots.") # Debugging tool
        return players

    def fill_empty_slots(self):
        """Fills remaining slots with 'Open Slot' placeholders."""
        while len(self.players) < self.max_players:
            self.players.append("Open Slot")

        print(f"Updated players list for {self.name}: {self.players}") # Debugging tool

    def add_player(self, gamer_tag):
        """Adds a player to the first available open slot and updates rounds."""
        for i, player in enumerate(self.players):
            if player == "Open Slot":
                self.players[i] = gamer_tag  # Replace Open Slot with the player's gamertag
                print(f"Added player {gamer_tag} to slot {i}") # Debugging tool 
                self.generate_rounds()  # Recalculate rounds after a new player joins
                return True
        print(f"Tournament {self.name} is full. Could not add player {gamer_tag}") # Debugging tool
        return False  # Tournament is full

    def generate_rounds(self):
        """Generates a round-robin format tournament with table assignments."""
        print(f"Generating rounds inside RoundRobinTournament for: {self.name}") # Debugging tool

        if len(self.players) < 2:
            print("Not enough players to generate matchups. Using placeholders.") # Debugging tool
            self.players = ["Open Slot"] * self.max_players

        self.rounds.clear()
        players = self.players[:]
        print(f"Players before generating rounds: {players}") # Debugging tool

        if len(players) % 2 == 1:
            players.append("BYE")  # If odd players, add BYE to balance matchups
        
        num_rounds = len(players) - 1
        num_matches = len(players) // 2
        print(f"Total Rounds: {num_rounds}, Matches per Round: {num_matches}") # Debugging tool

        for round_num in range(num_rounds):
            round_matches = []
            for match_num in range(num_matches):
                p1 = players[match_num]
                p2 = players[-(match_num + 1)]
                table_num = (match_num % 2) + 1  # Assign table number (1 or 2)
                round_matches.append({"p1": p1, "p2": p2, "winner": None, "table": table_num})
            self.rounds.append(round_matches)
            print(f"Round {round_num + 1}: {round_matches}") # Debugging tool

            # Rotate players except for the first one (standard round-robin)
            players.insert(1, players.pop())
        print(f"Final generated rounds: {self.rounds}") # Debugging tool

    def update_winner(self, round_num, match_num, winner):
        """Updates the winner of a specific match."""
        self.rounds[round_num][match_num]["winner"] = winner
