import sqlite3
from PyQt6.QtWidgets import QMessageBox

class Tournament:
    """Base tournament class for different formats."""

    def __init__(self, name, max_players):
        self.name = name
        self.max_players = max_players
        self.players = self.load_registered_players()  # Fetch registered players
        self.rounds = []
    
    def load_registered_players(self):
        """Fetch players signed up for this tournament from the database."""
        conn = sqlite3.connect("src/game_cafe.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT registered_users.gamertag 
            FROM event_signup 
            JOIN registered_users ON event_signup.gamertag = registered_users.id 
            WHERE event_signup.event_name = ?
        """, (self.name,))
        
        players = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return players if players else []

    def set_winner(self, round_number, match, winner_gamertag):
        """Sets the winner for a match and updates the tournament bracket."""

        if not winner_gamertag or winner_gamertag == "Select Winner":
            return

        # Determine the loser
        loser_gamertag = match["p1"] if match["p2"] != winner_gamertag else match["p2"]

        # Update current match
        match["winner"] = winner_gamertag

        # Move the winner to the next round
        if round_number + 1 < len(self.rounds):
            next_match_index = self.rounds[round_number].index(match) // 2
            if self.rounds[round_number + 1][next_match_index]["p1"] == "TBD":
                self.rounds[round_number + 1][next_match_index]["p1"] = winner_gamertag
            else:
                self.rounds[round_number + 1][next_match_index]["p2"] = winner_gamertag

        # Handle Losers’ Bracket for Double Elimination
        if isinstance(self, DoubleEliminationTournament):
            self.move_to_losers_bracket(loser_gamertag, round_number)

        print(f"✅ Winner '{winner_gamertag}' has been set for Round {round_number}!")


    def move_to_losers_bracket(self, loser_gamertag, round_num):
        """Moves a losing player to the losers' bracket in a double elimination tournament."""
        if round_num < len(self.losers_bracket):  # Ensure the losers' bracket exists
            next_match_index = len(self.losers_bracket[round_num]) // 2
            
            if next_match_index < len(self.losers_bracket[round_num]):
                if "p1" not in self.losers_bracket[round_num][next_match_index] or \
                        self.losers_bracket[round_num][next_match_index]["p1"] == "TBD":
                    self.losers_bracket[round_num][next_match_index]["p1"] = loser_gamertag
                else:
                    self.losers_bracket[round_num][next_match_index]["p2"] = loser_gamertag


class SingleEliminationTournament(Tournament):
    """Single elimination format: lose once = eliminated."""
    def __init__(self, name, max_players):
        super().__init__(name, max_players)
        self.players = self.load_registered_players()  # Fetch registered players
        self.rounds = []

        print(f"Creating Single Elimination Tournament: {self.name} with max_players: {self.max_players}")
        print(f"Initial players list: {self.players}")

        self.fill_empty_slots()  # Ensure proper bracket structure
        self.generate_rounds()  # Generate tournament rounds

    def load_registered_players(self):
        """Fetches players signed up for this tournament from the database."""
        conn = sqlite3.connect("src/game_cafe.db")
        cursor = conn.cursor()

        # Correct JOIN using `registered_users.id` to match `event_signup.gamertag`
        cursor.execute("""
            SELECT registered_users.gamertag 
            FROM event_signup 
            JOIN registered_users ON event_signup.gamertag = registered_users.id 
            WHERE event_signup.event_name = ?
        """, (self.name,))
    
        players = [row[0] for row in cursor.fetchall()]
        conn.close()
    
        return players if players else []

    
    def fill_empty_slots(self):
        """Fills remaining slots with 'Open Slot' placeholders."""
        while len(self.players) < self.max_players:
            self.players.append("Open Slot")
        print(f"Updated players list for {self.name}: {self.players}")  # Debugging tool

    def generate_rounds(self):
        """Creates an initial single-elimination bracket structure."""
        self.rounds = []
        num_rounds = int(math.log2(self.max_players)) + 1  # Total rounds including finals

        # First round: Assign actual players
        first_round = []
        for i in range(0, self.max_players, 2):
            match = {"p1": self.players[i], "p2": self.players[i+1], "winner": None}
            first_round.append(match)
        self.rounds.append(first_round)

        # Generate future rounds with "TBD"
        num_matches = len(first_round) // 2
        for round_num in range(1, num_rounds):
            next_round = []
            for match_num in range(num_matches):
                next_round.append({
                    "p1": f"Winner of Match {match_num * 2 + 1}",
                    "p2": f"Winner of Match {match_num * 2 + 2}",
                    "winner": None
                })
            self.rounds.append(next_round)
            num_matches //= 2  # Reduce match count each round

class DoubleEliminationTournament(Tournament):
    """Double elimination format: Two losses before elimination."""
    
    def __init__(self, name, max_players):
        super().__init__(name, max_players)
        self.players = self.load_registered_players()  # Fetch registered players
        self.rounds = []
        self.winners_bracket = []
        self.losers_bracket = []
        self.grand_finals = None

        print(f"Creating Double Elimination Tournament: {self.name} with max_players: {self.max_players}")
        print(f"Initial players list: {self.players}")

        self.fill_empty_slots()
        self.generate_rounds()

    def load_registered_players(self):
        """Fetches players signed up for this tournament from the database."""
        conn = sqlite3.connect("src/game_cafe.db")
        cursor = conn.cursor()

        # Correct JOIN using `registered_users.id` to match `event_signup.gamertag`
        cursor.execute("""
            SELECT registered_users.gamertag 
            FROM event_signup 
            JOIN registered_users ON event_signup.gamertag = registered_users.id 
            WHERE event_signup.event_name = ?
        """, (self.name,))
    
        players = [row[0] for row in cursor.fetchall()]
        conn.close()
    
        return players if players else []


    def fill_empty_slots(self):
        """Fills remaining slots with 'Open Slot' placeholders."""
        while len(self.players) < self.max_players:
            self.players.append("Open Slot")
        print(f"Updated players list for {self.name}: {self.players}")

    def generate_rounds(self):
        """Generates the Winners' and Losers' brackets for a double-elimination tournament."""
        self.rounds = []

        num_rounds = int(math.log2(self.max_players)) + 1  # Rounds needed

        # First round: Assign actual players
        first_round = [{"p1": self.players[i], "p2": self.players[i+1], "winner": None, "loser": None}
                       for i in range(0, self.max_players, 2)]
        self.rounds.append(first_round)

        # Generate Winner's Bracket rounds
        num_matches = len(first_round) // 2
        for round_num in range(1, num_rounds):
            next_round = [{"p1": f"Winner of WB Round {round_num} Match {match_num * 2 + 1}",
                           "p2": f"Winner of WB Round {round_num} Match {match_num * 2 + 2}",
                           "winner": None, "loser": None}
                          for match_num in range(num_matches)]
            self.rounds.append(next_round)
            num_matches //= 2  # Reduce match count each round

class RoundRobinTournament(Tournament):
    """Round-robin format: Each player faces every other player once."""
    
    def __init__(self, name, max_players):
        super().__init__(name, max_players)
        self.players = self.load_registered_players()  # Fetch registered players
        self.rounds = []

        print(f"Creating RoundRobinTournament: {self.name} with max_players: {self.max_players}")
        print(f"Initial players list: {self.players}")

        self.fill_empty_slots()
        self.generate_rounds()

    def load_registered_players(self):
        """Fetches players signed up for this tournament from the database."""
        conn = sqlite3.connect("src/game_cafe.db")
        cursor = conn.cursor()

        # Correct JOIN using `registered_users.id` to match `event_signup.gamertag`
        cursor.execute("""
            SELECT registered_users.gamertag 
            FROM event_signup 
            JOIN registered_users ON event_signup.gamertag = registered_users.id 
            WHERE event_signup.event_name = ?
        """, (self.name,))
    
        players = [row[0] for row in cursor.fetchall()]
        conn.close()
    
        return players if players else []


    def fill_empty_slots(self):
        """Fills remaining slots with 'Open Slot' placeholders."""
        while len(self.players) < self.max_players:
            self.players.append("Open Slot")
        print(f"Updated players list for {self.name}: {self.players}")

    def generate_rounds(self):
        """Generates a round-robin format tournament with table assignments."""
        if len(self.players) < 2:
            self.players = ["Open Slot"] * self.max_players

        self.rounds.clear()
        players = self.players[:]

        if len(players) % 2 == 1:
            players.append("BYE")  # If odd players, add BYE to balance matchups
        
        num_rounds = len(players) - 1
        for round_num in range(num_rounds):
            round_matches = [{"p1": players[match_num], "p2": players[-(match_num + 1)], "winner": None, "table": (match_num % 2) + 1}
                             for match_num in range(len(players) // 2)]
            self.rounds.append(round_matches)

            # Rotate players except for the first one (standard round-robin)
            players.insert(1, players.pop())

        print(f"Final generated rounds: {self.rounds}")
