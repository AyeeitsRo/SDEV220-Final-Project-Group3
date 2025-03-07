class GameLibrary:
    """
    **GameLibrary Class**
    
    **Class Purpose:**
    - Stores and manages all games available at the cafe.
    - Uses a dictionary to store each game's **title, category, and image path**.
    
    **Why This Class Exists:**
    - Provides a **centralized** storage system for games.
    - Allows easy retrieval of game information for display in the UI.
    - Ensures game data remains **organized and accessible**.
    
    **Benefits to the Project:**
    - Makes it easy to **add or update games** in a single place.
    - Simplifies fetching game-related information dynamically.
    - Reduces **hardcoded game data** across multiple files, because it is centralized here.
    """
    
    def __init__(self):
        """
        **Initializes the GameLibrary and populates the games dictionary.**
        
        **Implementation Decisions:**
        - Uses a dictionary where:
          - The **key** is the game title.
          - The **value** is a list containing:
            1. The game **category** (e.g., 'competitive', 'campaign').
            2. The **image file path** for UI display.
        """
        
        # Dictionary named `games` containing all hosted games at the cafe.
        self.games: dict[str, list[str]] = {
            'chess': ['competitive', 'resources/images/chess.png'],
            'dnd': ['campaign', 'resources/images/dnd.png'],
            'magic': ['competitive', 'resources/images/magic.jpg'],
            'monopoly': ['competitive', 'resources/images/monopoly.jpg'],
            'pokemon': ['competitive', 'resources/images/pokemon.png'],
            'poker': ['competitive', 'resources/images/poker.png'],
            'risk': ['competitive', 'resources/images/risk.png'],
            'runescape': ['campaign', 'resources/images/runescape.jpg'],
            'warhammer': ['campaign', 'resources/images/warhammer.png'],
            'wow': ['campaign', 'resources/images/wow.png']
        }

    def display_games(self) -> list[str]:
        """
        **Returns a list of all available game names.**
        
        **Why This Function Exists:**
        - Provides a simple way to retrieve all games stored in `GameLibrary`.
        - Ensures the UI or other components can dynamically fetch game names.
        
        **Implementation Decisions:**
        - Uses `self.games.keys()` to extract game names efficiently.
        
        **Returns:**
        - A list of strings containing all game titles.
        """
        return list(self.games.keys())  # Extracts and returns all game titles from the dictionary
