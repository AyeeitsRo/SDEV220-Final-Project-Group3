from view.menu import MenuWindow
from view.tournament_display import TournamentDisplay
from view.game_library_display import GameDisplay

class Controller:
    def __init__(self):
        pass

    # Opens the game library      
    def open_game_library(self):
        print("Game Library opened") # Debugging tool
        self.game_library_display = GameDisplay()
        self.game_library_display.show()

    # Opens the tournaments window
    def open_tournaments(self):
        print("Tournaments opened") # Debugging tool
        self.tournament_view = TournamentDisplay()
        self.tournament_view.show()

    # Opens the menu for the cafe
    def open_cafe_menu(self):
        print("Café Menu opened") # Debugging tool
        self.menu_window = MenuWindow()
        self.menu_window.show()

if __name__ == "__main__":
    controller = Controller()
    controller.open_game_library()

