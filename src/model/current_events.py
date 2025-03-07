import sqlite3

class CurrentEvents:
    """
    **CurrentEvents Class**
    
    **Class Purpose:**
    - Manages and retrieves data related to **tournaments** and **campaigns** from the database.
    - Connects to an SQLite database to fetch relevant event information dynamically.
    
    **Why This Class Exists:**
    - Ensures **real-time access** to tournament and campaign data stored in a structured format.
    - Reduces reliance on **hardcoded event details** by dynamically pulling data from the database.
    - Allows easy expansion of event data without requiring changes to the application logic.
    """
    
    def __init__(self, db_path="src\game_cafe.db"):
        """ Initializes the CurrentEvents class and defines the database path. """
        self.db_path = db_path  # Assigns the database path to a variable for easier connections.
    
    def get_tournaments(self, game_name):
        """
        **Fetches tournament details for a specific game.**
        
        **Why This Function Exists:**
        - Retrieves tournament data dynamically instead of hardcoding it.
        - Ensures tournaments are fetched and displayed based on the selected game type.
        - Uses a structured query to retrieve relevant tournament details from the database.
        
        **Implementation Decisions:**
        - Uses parameterized queries to **prevent SQL injection**.
        - Fetches tournament details including event name, type, date, time, entry fee, prize, and max players.
        
        **Parameters:**
        - `game_name` (str): The game type to filter tournaments.
        
        **Returns:**
        - `list[dict]`: A list of tournament dictionaries with relevant details.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Establish Database Connection**
        2️⃣ **Step 2 - Execute SQL Query**
        3️⃣ **Step 3 - Process Query Results**
        4️⃣ **Step 4 - Close Database Connection**
        5️⃣ **Step 5 - Return Data**
        """
        conn = sqlite3.connect(self.db_path)  # Step 1: Establish connection to the database.
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands.

        cursor.execute("""
            SELECT event_name, game_type, event_type, date, time, entry_fee, prize, max_players
            FROM active_tournaments
            WHERE game_type = ?
        """, (game_name.lower(),))  # Step 2: Execute the query, filtering by the given game_name.

        # Step 3: Process the query results and convert them into dictionaries.
        tournaments = [
            {
                "name": row[0],  # Tournament name
                "game_type": row[1],  # Game type
                "type": row[2],  # Tournament format (e.g., single_elimination, double_elimination)
                "date": row[3],  # Date of the tournament
                "time": row[4],  # Time of the tournament
                "entry_fee": row[5],  # Entry fee amount
                "prize": row[6],  # Prize details
                "max_players": int(row[7]),  # Max number of players allowed
            }
            for row in cursor.fetchall()
        ]

        conn.close()  # Step 4: Close the database connection to free up resources.
        return tournaments  # Step 5: Return the list of tournaments.

    def get_campaigns(self, game_name):
        """
        **Fetches active campaigns for a specific game.**
        
        **Why This Function Exists:**
        - Campaigns are stored in a database and must be retrieved dynamically.
        - Fetches campaign details such as host, meeting time, and player limits for a given game.
        
        **Implementation Decisions:**
        - Uses parameterized queries to **prevent SQL injection**.
        - Retrieves campaign details including host, meeting time, and max players.
        
        **Parameters:**
        - `game_name` (str): The game type to filter campaigns.
        
        **Returns:**
        - `list[dict]`: A list of campaign dictionaries with relevant details.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Establish Database Connection**
           - Connects to the SQLite database using `sqlite3.connect()`.
        
        2️⃣ **Step 2 - Execute SQL Query**
           - Retrieves campaign details from the `active_campaigns` table.
           - Filters results based on the provided `game_name`.
        
        3️⃣ **Step 3 - Process Query Results**
           - Converts each retrieved row into a dictionary containing campaign details.
        
        4️⃣ **Step 4 - Close Database Connection**
           - Closes the connection to **free up resources**.
        
        5️⃣ **Step 5 - Return Data**
           - Returns a list of dictionaries, each representing a campaign.
        """
        conn = sqlite3.connect(self.db_path)  # Step 1: Establish connection to the database.
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands.

        cursor.execute("""
            SELECT campaign_name, game_type, host, meet_day, meet_frequency, time, max_players
            FROM active_campaigns
            WHERE game_type = ?
        """, (game_name.lower(),))  # Step 2: Execute query filtering by game_name.

        # Step 3: Process query results into dictionaries.
        campaigns = [
            {
                "name": row[0],  # Campaign name
                "game_type": row[1],  # Game type
                "host": row[2],  # Host of the campaign
                "meet_day": row[3],  # Meeting day
                "meet_frequency": row[4],  # How often they meet
                "time": row[5],  # Meeting time
                "max_players": int(row[6]),  # Maximum number of players
            }
            for row in cursor.fetchall()
        ]

        conn.close()  # Step 4: Close the database connection.
        return campaigns  # Step 5: Return the list of campaigns.
    
    def get_all_tournaments(self):
        """
        **Fetches all active tournaments from the database.**
        
        **Why This Function Exists:**
        - Provides a way to retrieve all tournaments instead of filtering by a specific game.
        - Ensures all tournament details are accessible from a single function call.
        
        **Implementation Decisions:**
        - Uses a direct SQL query to fetch all tournaments from `active_tournaments`.
        
        **Returns:**
        - `list[dict]`: A list of tournament dictionaries.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Establish Database Connection**
           - Connects to the SQLite database using `sqlite3.connect()`.
        
        2️⃣ **Step 2 - Execute SQL Query**
           - Retrieves tournament details from the `active_tournaments` table.
        
        3️⃣ **Step 3 - Process Query Results**
           - Converts each retrieved row into a dictionary containing tournament details.
        
        4️⃣ **Step 4 - Close Database Connection**
           - Closes the connection to **free up resources**.
        
        5️⃣ **Step 5 - Return Data**
           - Returns a list of dictionaries, each representing a tournament.
        """
        conn = sqlite3.connect(self.db_path)  # Step 1: Establish connection to the database.
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands.

        cursor.execute("""
            SELECT event_name, game_type, event_type, date, time, entry_fee, prize, max_players
            FROM active_tournaments
        """)  # Step 2: Execute query to fetch all tournaments.

        # Step 3: Process query results into dictionaries.
        tournaments = [
            {
                "name": row[0],  # Tournament name
                "game_type": row[1],  # Game type
                "type": row[2],  # Tournament type
                "date": row[3],  # Tournament date
                "time": row[4],  # Tournament time
                "entry_fee": row[5],  # Entry fee amount
                "prize": row[6],  # Prize details
                "max_players": int(row[7])  # Max number of players
            }
            for row in cursor.fetchall()
        ]

        conn.close()  # Step 4: Close the database connection.
        return tournaments  # Step 5: Return the list of tournaments.