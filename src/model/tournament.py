import math
import sqlite3

class Tournament:
    """Base tournament class for different formats."""

    def __init__(self, name, max_players):
        self.name = name
        self.max_players = max_players
        self.players = []  # List of gamer tags
        self.rounds = []  # Tournament bracket rounds
        #self.create_initial_bracket()

    #def create_initial_bracket(self):
        #"""Generates an empty bracket structure based on player count."""
        #self.rounds = [[] for _ in range(self.get_round_count())]
        #for i in range(self.max_players // 2):
            #self.rounds[0].append(("Open Slot", "Open Slot"))

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
    def __init__(self, name, max_players):
        super().__init__(name, max_players)
        self.players = self.load_registered_players()  # Fetch registered players
        self.rounds = []

        print(f"Creating Double Elimination Tournament: {self.name} with max_players: {self.max_players}")
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
        return players if players else []
    
    def fill_empty_slots(self):
        """Fills remaining slots with 'Open Slot' placeholders."""
        while len(self.players) < self.max_players:
            self.players.append("Open Slot")

        print(f"Updated players list for {self.name}: {self.players}") # Debugging tool

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

    
    def update_winner(self, round_num, match_num, winner):
        """Updates the winner of a specific match."""
        self.rounds[round_num][match_num]["winner"] = winner
        # Update the next round with the winner
        if round_num + 1 < len(self.rounds):
            next_match = match_num // 2  # Determine next match index
            if match_num % 2 == 0:
                self.rounds[round_num + 1][next_match]["p1"] = winner
            else:
                self.rounds[round_num + 1][next_match]["p2"] = winner
    

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

    def generate_rounds(self):
        """Generates the Winners' and Losers' brackets for a double-elimination tournament."""
        self.rounds = []
    
        # Keep track of all matches correctly for each round
        rounds_list = []  

        num_rounds = int(math.log2(self.max_players)) + 1  # Rounds needed

        # Step 1: Create the Winner's Bracket (WB)
        first_round = []
        for i in range(0, self.max_players, 2):
            match = {"p1": self.players[i], "p2": self.players[i + 1], "winner": None, "loser": None}
            first_round.append(match)
        rounds_list.append({"round": 1, "matches": first_round})

        # Step 2: Generate Winner's Bracket rounds
        num_matches = len(first_round) // 2
        for round_num in range(2, num_rounds + 1):
            next_round = []
            for match_num in range(num_matches):
                next_round.append({
                    "p1": f"Winner of WB Round {round_num - 1} Match {match_num * 2 + 1}",
                    "p2": f"Winner of WB Round {round_num - 1} Match {match_num * 2 + 2}",
                    "winner": None,
                    "loser": None
                })
            rounds_list.append({"round": round_num, "matches": next_round})
            num_matches //= 2  # Reduce match count

        # Step 3: Generate Losers' Bracket correctly
        lb_rounds = []
        lb_match_count = self.max_players // 4  # Initial match count for LB
        lb_round_number = 2  # LB starts appearing after WB Round 1
    
        while lb_match_count >= 1:
            lb_round_matches = []
            for match_num in range(lb_match_count):
                if lb_round_number == 2:
                    # First round of LB gets losers from WB Round 1
                    lb_round_matches.append({
                        "p1": f"Loser of WB Round 1 Match {match_num * 2 + 1}",
                        "p2": f"Loser of WB Round 1 Match {match_num * 2 + 2}",
                        "winner": None
                    })
                else:
                    # Future LB rounds get previous LB winners
                    lb_round_matches.append({
                        "p1": f"Winner of LB Round {lb_round_number - 1} Match {match_num * 2 + 1}",
                        "p2": f"Winner of LB Round {lb_round_number - 1} Match {match_num * 2 + 2}",
                        "winner": None
                    })
        
            lb_rounds.append({"round": lb_round_number, "matches": lb_round_matches})
            lb_match_count //= 2  # Reduce match count each round
            lb_round_number += 1

        # Step 4: Add Losers' rounds AFTER their corresponding WB round
        full_rounds = []
        for r in rounds_list:
            full_rounds.append(r)
            # Add LB matches **only after corresponding WB rounds** finish
            if r["round"] in [1, 2, 3]:  # Adjust this to sync correctly
                lb_round = next((lb for lb in lb_rounds if lb["round"] == r["round"] + 1), None)
                if lb_round:
                    full_rounds.append(lb_round)

        # Step 5: Add Grand Finals as the last round
        self.grand_finals = {
            "p1": "Winner of WB Finals",
            "p2": "Winner of LB Finals",
            "winner": None,
            "reset_match": False
        }
        full_rounds.append({
            "round": num_rounds,
            "matches": [{"p1": "Winner of WB Finals", "p2": "Winner of LB Finals", "winner": None, "reset_match": False}]
        })

        # Store final round structure
        self.rounds = full_rounds
        print(f"✅ Final Tournament Rounds: {self.rounds}")  # Debugging tool


    def update_winner(self, bracket_type, round_num, match_num, winner):
        """Updates a match winner and advances them in the correct bracket."""
    
        if bracket_type == "winners":
            match = self.winners_bracket[round_num][match_num]
            match["winner"] = winner
            match["loser"] = match["p1"] if match["p2"] == winner else match["p2"]

            # Move loser to the corresponding Losers' Bracket round
            if round_num < len(self.losers_bracket):  # Ensure we have a valid LB round
                lb_round = round_num  # The LB round number is usually the same as the WB round
                lb_match = match_num // 2  # Determine correct match position

                if match_num % 2 == 0:
                    self.losers_bracket[lb_round][lb_match]["p1"] = match["loser"]
                else:
                    self.losers_bracket[lb_round][lb_match]["p2"] = match["loser"]

        elif bracket_type == "losers":
            match = self.losers_bracket[round_num][match_num]
            match["winner"] = winner
            # If a player loses in the Losers' Bracket, they are eliminated

        elif bracket_type == "grand_finals":
            self.grand_finals["winner"] = winner
        
            # If the Losers' Bracket finalist wins, trigger a **reset match**
            if self.grand_finals["p2"] == winner:
                self.grand_finals["reset_match"] = True
                print("🏆 Grand Finals Reset! The Losers' Bracket winner must win one more time.")

        print(f"✅ Updated Brackets: WB: {self.winners_bracket}, LB: {self.losers_bracket}")

class RoundRobinTournament(Tournament):
    def __init__(self, name, max_players):
        super().__init__(name, max_players)
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
