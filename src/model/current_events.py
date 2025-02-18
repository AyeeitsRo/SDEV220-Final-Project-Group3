from model.game_library import GameLibrary  # Import GameLibrary for images

class CurrentEvents:
    """
    A class to manage and retrieve cafe-hosted events, including tournaments and campaigns.
    
    Attributes:
        tournaments (dict): A dictionary containing tournament data for each game.
        campaigns (dict): A dictionary containing open campaign session data for each game.
    """

    def __init__(self):
        """Initializes the CurrentEvents class, loads tournament and campaign data. """

        # Dictionary of cafe-hosted tournaments: {game_name: [list of tournaments]}
        self.tournaments = {
            "chess": [
                {"name": "Cafe Chess Masters", "date": "2025-03-10", "time": "6:00 PM", "entry_fee": "$10", "prize": "$500", "max_players": 8, "type": "single_elimination"},
                {"name": "Blitz Night", "date": "2025-03-15", "time": "8:00 PM", "entry_fee": "$5", "prize": "Free Drinks", "max_players": 4, "type": "round_robin"}
            ],
            "magic": [
                {"name": "MTG Friday Night Magic", "date": "2025-03-22", "time": "7:00 PM", "entry_fee": "$15", "prize": "Store Credit", "max_players": 16, "type": "double_elimination"}
            ],
            "poker": [
                {"name": "Poker Night", "date": "2025-03-05", "time": "9:00 PM", "entry_fee": "$20", "prize": "$1000 Pot", "max_players": 6, "type": "round_robin"}
            ]
        }


        # Dictionary of open campaign sessions at the cafe: {game_name: [list of campaigns]}
        self.campaigns = {
            "dnd": [
                {"name": "Lost Mine of Phandelver", "date": "02-20-2025", "time": "5:00 PM", "dm": "John", "players_needed": 2},
                {"name": "Strixhaven Academy", "date": "03-02-2025", "time": "7:00 PM", "dm": "Sarah", "players_needed": 3}
            ],
            "warhammer": [
                {"name": "Warhammer 40k: Cafe Battle", "date": "02-28-2025", "time": "6:30 PM", "dm": "Alex", "players_needed": 1}
            ]
        }

    def get_tournaments(self, game_name):
        """
        Retrieves a list of upcoming cafe-hosted tournaments for a given game.
        
        Args:
            game_name (str): The name of the game for which tournaments should be retrieved.
        
        Returns:
            list[dict]: A list of dictionaries, each representing a tournament with details such as 
                        name, date, time, entry fee, prize, and associated game image.
        """
        game_name = game_name.lower()
        tournaments = self.tournaments.get(game_name, [])  # Retrieve tournaments for the given game

        return tournaments

    def get_campaigns(self, game_name):
        """
        Retrieves a list of open cafe-hosted campaign sessions for a given game.
        
        Args:
            game_name (str): The name of the game for which campaigns should be retrieved.
        
        Returns:
            list[dict]: A list of dictionaries, each representing a campaign session with details such as 
                        name, date, time, DM (Dungeon Master), and number of players needed.
        """
        game_name = game_name.lower()
        campaigns = self.campaigns.get(game_name, [])  # Retrieve campaigns for the given game

        return campaigns


