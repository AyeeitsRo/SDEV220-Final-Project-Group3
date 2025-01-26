from modules.tournament import Tournament

class SingleEliminationTournament(Tournament):
    def __init__(self, name, date, location, participants):
        super().__init__(name, date, location)
        self.participants = participants


    def create(self):
        pass
