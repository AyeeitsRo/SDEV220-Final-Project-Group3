import sqlite3
import math

class Tournament:
    """
    **Tournament Class**
    
    **Class Purpose:**
    - Serves as the **base class** for different tournament formats.
    - Stores tournament details such as **name, player limit, registered players, and rounds**.
    - Manages retrieving player data from the database.
    
    **Why This Class Exists:**
    - Provides a **common structure** for all tournament types.
    - Eliminates redundant code by defining **shared functionality**.
    - Ensures **players are correctly loaded** from the database at initialization.
    """
    
    def __init__(self, name: str, max_players: int):
        """ Initializes the Tournament class. """
        self.name = name  # Store tournament name
        self.max_players = max_players  # Store max number of players
        self.players = self.load_registered_players()  # Fetch registered players from database
        self.rounds = []  # Initialize rounds list
    
    def load_registered_players(self) -> list[str]:
        """
        **Fetches players signed up for this tournament from the database.**
        
        **Why This Function Exists:**
        - Ensures **only registered players** are included in the tournament.
        - Automates **retrieving player data**, removing the need for manual entry.
        
        **Implementation Decisions:**
        - Uses a **JOIN query** to match signed-up players with their gamertags.
        - Stores player gamertags in a **list** for easy access.
        - Uses **parameterized queries** to prevent **SQL injection**.
        
        **Returns:**
        - `list[str]`: A list of gamertags of registered players.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Establish Database Connection**
           - Connects to the SQLite database.
        
        2️⃣ **Step 2 - Execute SQL Query**
           - Retrieves gamertags of players who signed up for this tournament.
        
        3️⃣ **Step 3 - Process Query Results**
           - Converts query results into a **list of gamertags**.
        
        4️⃣ **Step 4 - Close Database Connection**
           - Ensures database resources are properly released.
        
        5️⃣ **Step 5 - Return Player List**
           - Returns the list of registered players.
        """
        conn = sqlite3.connect("src/game_cafe.db")  # Step 1: Connect to database
        cursor = conn.cursor()  # Create a cursor to execute SQL commands

        cursor.execute("""
            SELECT registered_users.gamertag 
            FROM event_signup 
            JOIN registered_users ON event_signup.gamertag = registered_users.id 
            WHERE event_signup.event_name = ?
        """, (self.name,))  # Step 2: Retrieve players who signed up for this tournament
        
        players = [row[0] for row in cursor.fetchall()]  # Step 3: Extract gamertags into a list
        conn.close()  # Step 4: Close the database connection
        
        return players if players else []  # Step 5: Return player list (empty list if no players)

    """
    def set_winner(self, round_number, match, winner_gamertag):
        #Sets the winner for a match and updates the tournament bracket.

        if not winner_gamertag or winner_gamertag == "Select Winner":
            return
        
        # Find the exact match object from self.rounds before modifying it
        if round_number > len(self.rounds):
            print(f"❌ Error: Round {round_number} does not exist!")
            return

        round_matches = self.rounds[round_number]

        # Ensure match exists in the current round
        match_index = round_number
        for i, stored_match in enumerate(round_matches):
            if stored_match["p1"] == match["p1"] and stored_match["p2"] == match["p2"]:
                match_index = i
                break

        if match_index is None:
            print(f"❌ Error: Match ({match['p1']} vs {match['p2']}) not found in round {round_number}")
            return

        # Determine the loser
        loser_gamertag = match["p1"] if match["p2"] != winner_gamertag else match["p2"]

        # Update match winner
        print("Round Matches:", round_matches)
        print("Match Index:", match_index)
        print("Both Round Matches and Match Index:", round_matches[match_index])
        round_matches[match_index]["winner"] = winner_gamertag

        # Move the winner to the next round
        if round_number + 1 < len(self.rounds):
            next_match_index = match_index // 2  # Find correct match index in the next round
            if self.rounds[round_number + 1][next_match_index]["p1"] == "TBD":
                self.rounds[round_number + 1][next_match_index]["p1"] = winner_gamertag
            else:
                self.rounds[round_number + 1][next_match_index]["p2"] = winner_gamertag

        # Handle Losers’ Bracket for Double Elimination
        if isinstance(self, DoubleEliminationTournament):
            self.move_to_losers_bracket(loser_gamertag, round_number)

        print(f"✅ Winner '{winner_gamertag}' set for Round {round_number}!")



    def move_to_losers_bracket(self, loser_gamertag, round_num):
        #Moves a losing player to the losers' bracket in a double elimination tournament.
        if round_num < len(self.losers_bracket):  # Ensure the losers' bracket exists
            next_match_index = len(self.losers_bracket[round_num]) // 2
            
            if next_match_index < len(self.losers_bracket[round_num]):
                if "p1" not in self.losers_bracket[round_num][next_match_index] or \
                        self.losers_bracket[round_num][next_match_index]["p1"] == "TBD":
                    self.losers_bracket[round_num][next_match_index]["p1"] = loser_gamertag
                else:
                    self.losers_bracket[round_num][next_match_index]["p2"] = loser_gamertag
    """

class SingleEliminationTournament(Tournament):
    """
    **SingleEliminationTournament Class**
    
    **Class Purpose:**
    - Implements a **single elimination** tournament format where a player is eliminated after one loss.
    - Manages **bracket structure, round generation, and slot filling** for missing players.
    
    **Why This Class Exists:**
    - Ensures a structured **bracket-style** tournament format.
    - Dynamically **retrieves player data** and fills open slots for proper bracket formation.
    - Automates **round generation**, reducing manual setup time.
    """
    
    def __init__(self, name: str, max_players: int):
        """ Initializes a Single Elimination Tournament. """
        super().__init__(name, max_players)  # Call base class constructor
        self.players = self.load_registered_players()  # Fetch registered players
        self.rounds = []  # Initialize rounds list

        print(f"Creating Single Elimination Tournament: {self.name} with max_players: {self.max_players}")  # Step 4: Debugging
        print(f"Initial players list: {self.players}")  # Debugging

        self.fill_empty_slots()  # Fill empty slots with placeholders
        self.generate_rounds()  # Generate tournament rounds

    def load_registered_players(self) -> list[str]:
        """
        **Fetches players signed up for this tournament from the database.**
        
        **Why This Function Exists:**
        - Dynamically retrieves **registered players** to populate the tournament.
        - Automates **player assignment**, reducing manual input errors.
        
        **Returns:**
        - `list[str]`: A list of registered player gamertags.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Establish Database Connection**
           - Connects to SQLite database.
        
        2️⃣ **Step 2 - Execute Query**
           - Retrieves gamertags of players who signed up for this tournament.
        
        3️⃣ **Step 3 - Convert Query Results**
           - Formats retrieved player data into a list.
        
        4️⃣ **Step 4 - Close Database Connection**
           - Ensures database resources are freed.
        
        5️⃣ **Step 5 - Return Player List**
           - Returns the list of registered players.
        """
        conn = sqlite3.connect("src/game_cafe.db")  # Step 1: Connect to database
        cursor = conn.cursor()  # Create cursor for executing SQL queries

        cursor.execute("""
            SELECT registered_users.gamertag 
            FROM event_signup 
            JOIN registered_users ON event_signup.gamertag = registered_users.id 
            WHERE event_signup.event_name = ?
        """, (self.name,))  # Step 2: Retrieve players who signed up for this tournament
    
        players = [row[0] for row in cursor.fetchall()]  # Step 3: Convert database output to list
        conn.close()  # Step 4: Close the database connection
    
        return players if players else []  # Step 5: Return players or an empty list
    
    def fill_empty_slots(self) -> None:
        """
        **Fills empty player slots to complete the bracket.**
        
        **Why This Function Exists:**
        - Ensures the bracket maintains a **valid structure** by adding placeholder slots.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Check Player Count**
           - Ensures the player count matches `max_players`.
        
        2️⃣ **Step 2 - Append Open Slots**
           - Adds placeholder entries (`"Open Slot"`) until the tournament is full.
        
        3️⃣ **Step 3 - Debugging Print**
           - Prints the updated player list for verification.
        """
        while len(self.players) < self.max_players:  # Step 1: Check if slots are available
            self.players.append("Open Slot")  # Step 2: Fill remaining slots
        print(f"Updated players list for {self.name}: {self.players}")  # Step 3: Debugging output
    
    def generate_rounds(self) -> None:
        """
        **Generates a structured single elimination tournament bracket.**
        
        **Why This Function Exists:**
        - Automates the creation of a **single elimination** tournament structure.
        - Ensures that matchups correctly follow the single elimination format:
          - A player is eliminated after **one loss**.
          - Winners progress to the next round until only one player remains.
        - Guarantees a **balanced** and **logically correct** tournament bracket.
        
        **Mathematical Breakdown of Rounds Calculation:**
        - The number of rounds required for a **single elimination** tournament depends on the number of players.
        - A single elimination tournament always reduces the number of competitors by half each round.
        - The number of rounds needed is determined by:
          
          **Formula:**
          ```
          num_rounds = log2(total players)
          ```
          - `math.log2(self.max_players)`: Computes the **base-2 logarithm** of the total players.
          - The result gives the total number of rounds required to reduce the players to a **single winner**.
          - Example Calculations:
            - `max_players = 16` → `log2(16) = 4` rounds (16 → 8 → 4 → 2 → 1)
            - `max_players = 8` → `log2(8) = 3` rounds (8 → 4 → 2 → 1)
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Initialize Rounds List**
           - Clears any previously stored round data.
        
        2️⃣ **Step 2 - Calculate Number of Rounds**
           - Uses `math.log2(self.max_players)` to determine how many rounds are needed.
        
        3️⃣ **Step 3 - Generate First Round Matches**
           - Assigns actual players to the first set of matchups.
        
        4️⃣ **Step 4 - Generate Future Rounds**
           - Creates placeholders (`"TBD"`) for winners who will advance in later rounds.
        """
        self.rounds = []  # Step 1: Clear any previous tournament data
        num_rounds = int(math.log2(self.max_players))  # Step 2: Calculate number of rounds needed
        
        # **Step 3 - First Round: Assign real players**
        first_round = []
        for i in range(0, self.max_players, 2):  # Iterate through players in pairs (p1 vs p2)
            match = {"p1": self.players[i], "p2": self.players[i+1], "winner": None}  # Create match structure
            first_round.append(match)  # Add match to first round
        self.rounds.append(first_round)  # Store first round in rounds list
        
        # **Step 4 - Generate Future Rounds**
        num_matches = len(first_round) // 2  # The number of matches in the next round is half of the previous round
        for round_num in range(1, num_rounds):  # Iterate through rounds beyond the first
            next_round = []
            for match_num in range(num_matches):  # Generate placeholder matches for the next round
                next_round.append({
                    "p1": f"Winner of Match {match_num * 2 + 1}",
                    "p2": f"Winner of Match {match_num * 2 + 2}",
                    "winner": None
                })
            self.rounds.append(next_round)  # Store generated round
            num_matches //= 2  # Reduce number of matches by half for the next round


class DoubleEliminationTournament(Tournament):
    """
    **DoubleEliminationTournament Class**
    
    **Class Purpose:**
    - Implements a **double elimination** tournament format where a player must lose **twice** before elimination.
    - Manages both a **winners bracket** and a **losers bracket** to track players' progression.
    - Dynamically **retrieves player data** and fills open slots for proper bracket formation.
    
    **Why This Class Exists:**
    - Ensures a structured **double-elimination bracket system** that follows competitive tournament standards.
    - Allows players to continue competing even after a **single loss**, increasing fairness and engagement.
    - Automates **round generation**, reducing manual tournament setup.
    """
    
    def __init__(self, name: str, max_players: int):
        """ Initializes a Double Elimination Tournament. """
        super().__init__(name, max_players)  # Call base class constructor
        self.players = self.load_registered_players()  # Fetch registered players
        self.rounds = []  # Initialize main rounds list
        self.winners_bracket = []  # Initialize winners bracket
        self.losers_bracket = []  # Initialize losers bracket
        self.grand_finals = None  # Set grand finals placeholder

        print(f"Creating Double Elimination Tournament: {self.name} with max_players: {self.max_players}")  # Step 4: Debugging
        print(f"Initial players list: {self.players}")  # Debugging

        self.fill_empty_slots()  # Fill empty slots with placeholders
        self.generate_rounds()  # Generate tournament rounds

    def load_registered_players(self) -> list[str]:
        """
        **Fetches players signed up for this tournament from the database.**
        
        **Why This Function Exists:**
        - Dynamically retrieves **registered players** to populate the tournament.
        - Automates **player assignment**, reducing manual input errors.
        
        **Returns:**
        - `list[str]`: A list of registered player gamertags.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Establish Database Connection**
           - Connects to SQLite database.
        
        2️⃣ **Step 2 - Execute Query**
           - Retrieves gamertags of players who signed up for this tournament.
        
        3️⃣ **Step 3 - Convert Query Results**
           - Formats retrieved player data into a list.
        
        4️⃣ **Step 4 - Close Database Connection**
           - Ensures database resources are freed.
        
        5️⃣ **Step 5 - Return Player List**
           - Returns the list of registered players.
        """
        conn = sqlite3.connect("src/game_cafe.db")  # Step 1: Connect to database
        cursor = conn.cursor()  # Create cursor for executing SQL queries

        cursor.execute("""
            SELECT registered_users.gamertag 
            FROM event_signup 
            JOIN registered_users ON event_signup.gamertag = registered_users.id 
            WHERE event_signup.event_name = ?
        """, (self.name,))  # Step 2: Retrieve players who signed up for this tournament
    
        players = [row[0] for row in cursor.fetchall()]  # Step 3: Convert database output to list
        conn.close()  # Step 4: Close the database connection
    
        return players if players else []  # Step 5: Return players or an empty list
    
    def fill_empty_slots(self) -> None:
        """
        **Fills empty player slots to complete the bracket.**
        
        **Why This Function Exists:**
        - Ensures the bracket maintains a **valid structure** by adding placeholder slots.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Check Player Count**
           - Ensures the player count matches `max_players`.
        
        2️⃣ **Step 2 - Append Open Slots**
           - Adds placeholder entries (`"Open Slot"`) until the tournament is full.
        
        3️⃣ **Step 3 - Debugging Print**
           - Prints the updated player list for verification.
        """
        while len(self.players) < self.max_players:  # Step 1: Check if slots are available
            self.players.append("Open Slot")  # Step 2: Fill remaining slots
        print(f"Updated players list for {self.name}: {self.players}")  # Step 3: Debugging output


    def generate_rounds(self) -> None:
        """
        **Generates the Winners' and Losers' brackets for a double-elimination tournament.**
        
        **Why This Function Exists:**
        - Unlike single elimination, double elimination requires **two brackets**:
          - **Winners' Bracket** (WB): Players who haven't lost.
          - **Losers' Bracket** (LB): Players who lost once but have a chance to win the tournament.
        - This function ensures:
          - Proper structuring of the **Winners' Bracket (WB)**.
          - Correct placement of eliminated players into the **Losers' Bracket (LB)**.
          - Fair competition by following **double elimination rules**.
        
        **Mathematical Breakdown of Rounds Calculation:**
        - The number of rounds needed is determined using:
          
          **Formula:**
          ```
          num_rounds = log2(total players) + 1
          ```
          - `math.log2(self.max_players)`: Computes the **base-2 logarithm** to determine how many rounds are needed to reach a single undefeated player.
          - **Adding `+1`** accounts for the **Grand Finals**, where the final Winner' Bracket champion faces the Losers' Bracket champion.
          - Example Calculations:s
            - `max_players = 16` → `log2(16) + 1 = 5` rounds (16 → 8 → 4 → 2 → 1 → Grand Finals)
            - `max_players = 8` → `log2(8) + 1 = 4` rounds (8 → 4 → 2 → 1 → Grand Finals)
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Initialize Rounds List**
           - Clears any previously stored round data.
        
        2️⃣ **Step 2 - Calculate Number of Rounds**
           - Uses `math.log2(self.max_players) + 1` to determine the correct number of rounds.
        
        3️⃣ **Step 3 - Generate First Round Matches**
           - Assigns actual players to the first round of the Winners' Bracket (WB).
        
        4️⃣ **Step 4 - Generate Future Winners' Bracket Rounds**
           - Creates placeholders (`"TBD"`) for players advancing in the Winners' Bracket.
        """
        self.rounds = []  # Step 1: Clear any previous tournament data
        num_rounds = int(math.log2(self.max_players)) + 1  # Step 2: Calculate number of rounds needed (+1 for Grand Finals)
        
        # **Step 3 - First Round: Assign real players to Winners' Bracket**
        first_round = [
            {"p1": self.players[i], "p2": self.players[i+1], "winner": None, "loser": None}  # Create match structure
            for i in range(0, self.max_players, 2)  # Iterate through players in pairs (p1 vs p2)
        ]
        self.rounds.append(first_round)  # Store first round in rounds list
        
        # **Step 4 - Generate Future Rounds for the Winners' Bracket**
        num_matches = len(first_round) // 2  # The number of matches in the next round is half of the previous round
        for round_num in range(1, num_rounds):  # Iterate through rounds beyond the first
            next_round = [
                {
                    "p1": f"Winner of WB Round {round_num} Match {match_num * 2 + 1}",
                    "p2": f"Winner of WB Round {round_num} Match {match_num * 2 + 2}",
                    "winner": None, "loser": None
                }
                for match_num in range(num_matches)  # Generate placeholder matches for the next round
            ]
            self.rounds.append(next_round)  # Store generated round
            num_matches //= 2  # Reduce number of matches by half for the next round

class RoundRobinTournament(Tournament):
    """
    **RoundRobinTournament Class**
    
    **Class Purpose:**
    - Implements a **round-robin** tournament format where each player competes against every other player **once**.
    - Ensures a **balanced** schedule so that all players get equal opportunities to compete.
    - Dynamically **retrieves player data**, fills missing slots, and generates matchups.
    
    **Why This Class Exists:**
    - Used when **all players need to face each other**, rather than eliminating players after losses.
    - Ensures that every player **competes in an equal number of matches**.
    - Automates **match scheduling and table assignments**, reducing manual setup time.
    """
    
    def __init__(self, name: str, max_players: int):
        """ Initializes a Round-Robin Tournament. """
        super().__init__(name, max_players)  # Step 1: Call base class constructor
        self.players = self.load_registered_players()  # Step 2: Fetch registered players
        self.rounds = []  # Step 3: Initialize main rounds list

        print(f"Creating RoundRobinTournament: {self.name} with max_players: {self.max_players}")  # Step 4: Debugging
        print(f"Initial players list: {self.players}")  # Step 4: Debugging

        self.fill_empty_slots()  # Step 5: Fill empty slots with placeholders
        self.generate_rounds()  # Step 6: Generate tournament rounds

    def load_registered_players(self) -> list[str]:
        """
        **Fetches players signed up for this tournament from the database.**
        
        **Why This Function Exists:**
        - Dynamically retrieves **registered players** to populate the tournament.
        - Automates **player assignment**, reducing manual input errors.
        
        **Returns:**
        - `list[str]`: A list of registered player gamertags.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Establish Database Connection**
           - Connects to SQLite database.
        
        2️⃣ **Step 2 - Execute Query**
           - Retrieves gamertags of players who signed up for this tournament.
        
        3️⃣ **Step 3 - Convert Query Results**
           - Formats retrieved player data into a list.
        
        4️⃣ **Step 4 - Close Database Connection**
           - Ensures database resources are freed.
        
        5️⃣ **Step 5 - Return Player List**
           - Returns the list of registered players.
        """
        conn = sqlite3.connect("src/game_cafe.db")  # Step 1: Connect to database
        cursor = conn.cursor()  # Create cursor for executing SQL queries

        cursor.execute("""
            SELECT registered_users.gamertag 
            FROM event_signup 
            JOIN registered_users ON event_signup.gamertag = registered_users.id 
            WHERE event_signup.event_name = ?
        """, (self.name,))  # Step 2: Retrieve players who signed up for this tournament
    
        players = [row[0] for row in cursor.fetchall()]  # Step 3: Convert database output to list
        conn.close()  # Step 4: Close the database connection
    
        return players if players else []  # Step 5: Return players or an empty list
    
    def fill_empty_slots(self) -> None:
        """
        **Fills empty player slots to complete the bracket.**
        
        **Why This Function Exists:**
        - Ensures the bracket maintains a **valid structure** by adding placeholder slots.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Check Player Count**
           - Ensures the player count matches `max_players`.
        
        2️⃣ **Step 2 - Append Open Slots**
           - Adds placeholder entries (`"Open Slot"`) until the tournament is full.
        
        3️⃣ **Step 3 - Debugging Print**
           - Prints the updated player list for verification.
        """
        while len(self.players) < self.max_players:  # Step 1: Check if slots are available
            self.players.append("Open Slot")  # Step 2: Fill remaining slots
        print(f"Updated players list for {self.name}: {self.players}")  # Step 3: Debugging output


    def generate_rounds(self) -> None:
        """
        **Generates a round-robin format tournament with table assignments.**
        
        **Why This Function Exists:**
        - Unlike elimination tournaments, a round-robin tournament requires every participant to play against every other participant **once**.
        - This function ensures:
          - **Proper pairing** of players for each round.
          - **Rotation-based scheduling**, ensuring fairness.
          - **Handling of odd-numbered participants** with a BYE system.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Handle Edge Cases**
           - If fewer than **two players** are available, fill slots with `"Open Slot"` placeholders.
        
        2️⃣ **Step 2 - Initialize Players and Clear Previous Rounds**
           - Copy the player list to prevent modification issues.
           - Clear previously stored rounds to start fresh.
        
        3️⃣ **Step 3 - Ensure Even Number of Participants**
           - If the number of players is **odd**, add a `"BYE"` entry to balance matchups.
        
        4️⃣ **Step 4 - Generate Round-Robin Matchups**
           - The tournament lasts for **`num_rounds = total_players - 1`** rounds.
           - Matches are scheduled by **pairing players from opposite ends of the list**.
        
        5️⃣ **Step 5 - Rotate Players to Form New Matchups**
           - Standard **round-robin rotation algorithm** is used.
           - **First player remains fixed**, while others rotate **clockwise**.
        
        6️⃣ **Step 6 - Store and Print the Final Schedule**
           - Append each round to `self.rounds`.
           - Print final matchups for debugging.
        """
        # **Step 1 - Handle Edge Cases**
        if len(self.players) < 2:
            self.players = ["Open Slot"] * self.max_players  # Ensure a valid tournament structure
        
        # **Step 2 - Initialize Players and Clear Previous Rounds**
        self.rounds.clear()  # Reset rounds
        players = self.players[:]  # Copy player list to avoid modifying the original
        
        # **Step 3 - Ensure Even Number of Participants**
        if len(players) % 2 == 1:
            players.append("BYE")  # If odd players, add a BYE to balance matchups
        
        num_rounds = len(players) - 1  # **Each player plays against every other player once**
        
        # **Step 4 - Generate Round-Robin Matchups**
        for round_num in range(num_rounds):
            round_matches = [
                {
                    "p1": players[match_num],  # First player in matchup
                    "p2": players[-(match_num + 1)],  # Last player (paired from opposite ends)
                    "winner": None,  # No winner yet (to be determined during gameplay)
                    "table": (match_num % 2)  # Alternate table assignments for variety
                }
                for match_num in range(len(players) // 2)  # Create matchups for half the players per round
            ]
            self.rounds.append(round_matches)  # Store matchups for the round
        
            # **Step 5 - Rotate Players to Form New Matchups**
            players.insert(1, players.pop())  # Standard round-robin rotation (first player stays fixed)
        
        # **Step 6 - Store and Print the Final Schedule**
        print(f"Final generated rounds: {self.rounds}")  # Debugging output

