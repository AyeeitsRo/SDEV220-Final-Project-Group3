from view.menu import MenuWindow
from model.order import *
from view.tournament_display import TournamentDisplay
from view.game_library_display import GameDisplay
from model.current_events import CurrentEvents
from view.events_display import EventsDisplay, AllEventsDisplay, EventSignUp

class Controller:
    """
    Controller class 
    This class manages the interaction between views and click events in the GUI
    """

    def __init__(self):
        """Initialize the controller and load current events."""
        self.events = CurrentEvents() # Class in model/current_events.py
        self.order = Order() # Class in model/order.py

    def open_game_library(self):
        """Opens the Game Library window."""
        print("Game Library opened")  # Debugging tool, if this function is successfully called, this line will print to the terminal
        self.game_library_display = GameDisplay(self) # Class in view/game_library.py
        self.game_library_display.show() # Opens the GUI window

    def open_tournaments(self):
        """Opens the Tournaments window."""
        print("Tournaments opened")  # Debugging tool, if this function is successfully called, this line will print to the terminal
        self.tournament_view = TournamentDisplay(self) # Class in view/tournament_display.py
        self.tournament_view.show() # Opens the GUI window

    def open_cafe_menu(self):
        """Opens the Cafe Menu window."""
        print("Café Menu opened")  # Debugging tool, if this function is successfully called, this line will print to the terminal
        self.menu_window = MenuWindow(self) # Class in view/menu.py
        self.menu_window.show() # Opens the GUI window

    def on_game_clicked(self, game_name):
        """Opens the Events Display for a specific game.

        Args:
            game_name (str): The name of the game for which event should be displayed.
        """
        print(f"--- {game_name.upper()} Events at the Cafe ---") # Debugging tool, the name of the game clicked should print if this is working correctly.
        self.event_window = EventsDisplay(game_name, self) # Class in view/events_display.py
        # The order of the above arguments matter, game_name comes before controller(self)
        self.event_window.show() # Opens the GUI window

    def open_events(self):
        """Opens the All Events display window, showing all upcoming events at the cafe."""
        print("Opening All Events Window")  # Debugging tool, if this function is successfully called, this line will print to the terminal
        self.all_events = AllEventsDisplay(self)  # Class in view/events_display.py
        self.all_events.show()  # Opens the GUI window

    def on_signup(self, event, event_type):
        """Opens the sign up windown for the user to sign up for the associated event."""
        self.sign_up = EventSignUp(self, event, event_type) # Class in view/events_display.py
        self.sign_up.show() # Opens the GUI window
            
    def add_to_cart(self, item):
        """Adds item to the cart in menu.py"""
        # Check if the item already exists in the cart
        found = False
        for cart_item in order.items:
            if cart_item.name == item.name:  # Compare based on item name or unique identifier
                cart_item.quantity += 1  # Increment the quantity
                found = True
                break

        if not found:
            # If the item doesn't exist, add it to the cart as a new item
            order.add_item(item)

        self.menu_window.update_cart_ui()  # Update the cart UI after adding the item



    