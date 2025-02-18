class TournamentBracket:
    """Manages tournament standings and player progression."""

    def __init__(self, tournament):
        """
        Initializes a bracket for a given tournament.

        Args:
            tournament (Tournament): An instance of a Tournament subclass.
        """
        self.tournament = tournament
        self.bracket = tournament.display_bracket()
        self.results = {}

    def report_match_result(self, match_index, winner):
        """
        Updates the bracket with the match result.

        Args:
            match_index (int): Index of the match in the bracket.
            winner (str): Gamer tag of the winner.
        """
        if match_index < len(self.bracket):
            match = self.bracket[match_index]
            if winner in match:
                self.results[match_index] = winner
                self.advance_winner(match_index, winner)

    def advance_winner(self, match_index, winner):
        """Moves the winner forward to the next round."""
        next_round_index = match_index // 2
        if next_round_index >= len(self.bracket):
            self.bracket.append([winner, None])
        else:
            self.bracket[next_round_index][match_index % 2] = winner
