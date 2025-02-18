from view.menu import MenuWindow
from view.tournament_display import TournamentDisplay
from view.game_library_display import GameDisplay
from model.current_events import CurrentEvents
from view.events_display import EventsDisplay, AllEventsDisplay

class Controller:
    """
    Controller class 
    This class manages the interaction between views and click events in the GUI
    """

    def __init__(self):
        """Initialize the controller and load current events."""
        self.events = CurrentEvents() # Class in model/current_events.py

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

    def add_to_cart(self, item_name, item_price):
        """Adds item to the cart in menu.py"""
        print(f"{item_name} successfully added to the cart. \n Total: {item_price}")

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
        """
        Handles user sign-up for a tournament or campaign.

        Args:
            event_name (str): The name of the event (tournament or campaign).
            event_type (str): The type of event ('tournament' or 'campaign').
        """
        # If event is a dictionary, extract its name
        event_name = event["name"] if isinstance(event, dict) else event

        print(f"Attempting to sign up for: {event_name} ({event_type.capitalize()})")

        # Fetch event details from CurrentEvents
        current_events = CurrentEvents()

        if event_type == "tournament":
            events_list = current_events.tournaments
        elif event_type == "campaign":
            events_list = current_events.campaigns
        else:
            print("Invalid event type.")
            return

        # Find the specific event dictionary
        event_details = None
        for game, events in events_list.items():
            for e in events:
                if e["name"] == event_name:
                    event_details = e
                    break
            if event_details:
                break

        if event_details:
            print(f"User signed up for: {event_details['name']} ({event_type.capitalize()})")
            # TODO: Implement database storage or UI update here
        else:
            print("Event not found. Ensure the event name is correct.")
