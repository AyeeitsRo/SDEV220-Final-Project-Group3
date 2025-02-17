class GameLibrary:
    """
    This class is the game library, which stores each game hosted at the cafe.
    A dictionary is used to store each game and its data.
    The key is the game title, the first list item is the category, and the second list item is the file path to the photo.
    key : [list item 1, list item 2]     |      game title : [category, image file path]
    """
    def __init__(self):
        # Dictionary named games
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
        """Return a list of all game names."""
        return list(self.games.keys()) # Returns keys of dictionary since each key is set up as the game name

    