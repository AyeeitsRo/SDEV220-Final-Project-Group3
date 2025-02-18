import random

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
        import math
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
        self.players = []
        self.rounds = []

    def add_player(self, gamer_tag):
        """Adds a player if slots are available."""
        if len(self.players) < self.max_players:
            self.players.append(gamer_tag)
            self.generate_rounds()

    def generate_rounds(self):
        """Generates a round-robin format tournament with table assignments."""
        if len(self.players) < 2:
            return  # Need at least two players to form matches
        
        self.rounds.clear()
        players = self.players[:]
        if len(players) % 2 == 1:
            players.append("BYE")  # If odd players, add BYE
        
        num_rounds = len(players) - 1
        num_matches = len(players) // 2

        for round_num in range(num_rounds):
            round_matches = []
            for match_num in range(num_matches):
                p1 = players[match_num]
                p2 = players[-(match_num + 1)]
                table_num = (match_num % 2) + 1  # Assign table number (1 or 2)
                round_matches.append({"p1": p1, "p2": p2, "winner": None, "table": table_num})
            self.rounds.append(round_matches)

            # Rotate players except for the first one (standard round-robin)
            players.insert(1, players.pop())

    def update_winner(self, round_num, match_num, winner):
        """Updates the winner of a specific match."""
        self.rounds[round_num][match_num]["winner"] = winner


class SwissSystemTournament(Tournament):
    """Swiss system: players with similar records face off."""
    
    def generate_bracket(self):
        """Generates a Swiss-system bracket (initial random pairings)."""
        random.shuffle(self.players)
        self.bracket = [[self.players[i], self.players[i+1]] for i in range(0, len(self.players)-1, 2)]

