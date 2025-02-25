import sqlite3

class CurrentEvents:
    """
    A class to manage and retrieve events, including tournaments and campaigns.
    """

    def __init__(self, db_path="src\game_cafe.db"):
        """Initializes the CurrentEvents class and defines relative file path to database"""
        self.db_path = db_path # assigns the database path to a variable to make for easier connections.

    def get_tournaments(self, game_name):
        """
        Searches the database in the active_tournaments table and returns the data stored for the given tournament
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT event_name, game_type, event_type, date, time, entry_fee, prize, max_players
            FROM active_tournaments
            WHERE game_type = ?
        """, (game_name.lower(),))

        tournaments = [
            {
                "name": row[0],
                "game_type": row[1],
                "type": row[2],
                "date": row[3],
                "time": row[4],
                "entry_fee": row[5],
                "prize": row[6],
                "max_players": int(row[7]),
            }
            for row in cursor.fetchall()
        ]

        conn.close()
        return tournaments

    def get_campaigns(self, game_name):
        """
        Searches database table named active_campaigns, and gets a list of all active campaigns
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT campaign_name, game_type, host, meet_day, meet_frequency, time, max_players
            FROM active_campaigns
            WHERE game_type = ?
        """, (game_name.lower(),))

        campaigns = [
            {
                "name": row[0],
                "game_type": row[1],
                "host": row[2],
                "meet_day": row[3],
                "meet_frequency": row[4],
                "time": row[5],
                "max_players": int(row[6]),
            }
            for row in cursor.fetchall()
        ]

        conn.close()
        return campaigns
    
    def get_all_tournaments(self):
        """Fetches all active tournaments from the database instead of just one"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT event_name, game_type, event_type, date, time, entry_fee, prize, max_players
            FROM active_tournaments
        """)

        tournaments = [
            {
                "name": row[0],
                "game_type": row[1],
                "type": row[2],  
                "date": row[3],
                "time": row[4],
                "entry_fee": row[5],
                "prize": row[6],
                "max_players": int(row[7])
            }
            for row in cursor.fetchall()
        ]

        conn.close()
        return tournaments

