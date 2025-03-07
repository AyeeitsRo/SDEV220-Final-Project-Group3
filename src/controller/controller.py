from view.menu import MenuWindow
from model.order import *
from view.tournament_display import TournamentDisplay
from view.game_library_display import GameDisplay
from model.current_events import CurrentEvents
from view.events_display import EventsDisplay, AllEventsDisplay, EventSignUp

class Controller:
    """
    **Controller Class**
    
    **Class Purpose:**
    - Acts as the central hub that manages interactions between different views and user click events in the GUI.
    - Facilitates smooth communication between the **model** (data logic) and **view** (GUI display).
    - Ensures that the appropriate view or action is triggered when a user interacts with the interface.
    
    **Why This Class Exists:**
    - Instead of handling UI logic directly inside individual view classes, the **Controller** centralizes event handling.
    - Separating concerns improves code **maintainability, readability, and scalability**.
    - Simplifies debugging by allowing event handling and navigation logic to be traced from one location.
    
    **Benefits to the Project:**
    - Provides a **clean architecture** where views focus on displaying content while the controller manages interactions.
    - Reduces **circular dependencies** by having a **single point of reference** for event-driven actions.
    - Makes it easier to add **new features** without modifying existing views significantly.
    - Streamlines **import management**, ensuring that all required components are accessible through the controller.
    """
    
    def __init__(self):
        """Initialize the controller and load current events."""
        self.events = CurrentEvents()  # Handles event-related data retrieval
        self.order = Order()  # Manages orders in the cafe system

    def open_game_library(self):
        """Opens the Game Library window."""
        print("Game Library opened")  # Debugging output
        self.game_library_display = GameDisplay(self)  # Load game library UI
        self.game_library_display.show()  # Display window

    def open_tournaments(self):
        """Opens the Tournaments window."""
        print("Tournaments opened")
        self.tournament_view = TournamentDisplay(self)  # Load tournament UI
        self.tournament_view.show()  # Display window

    def open_cafe_menu(self):
        """Opens the Cafe Menu window."""
        print("Café Menu opened")  # Debugging output
        self.menu_window = MenuWindow(self)  # Load cafe menu UI
        self.menu_window.show()  # Display window

    def on_game_clicked(self, game_name):
        """Opens the Events Display for a specific game."""
        print(f"--- {game_name.upper()} Events at the Cafe ---")  # Debugging output
        self.event_window = EventsDisplay(game_name, self)  # Load event UI for the selected game
        self.event_window.show()  # Display window

    def open_events(self):
        """Opens the All Events display window, showing all upcoming events at the cafe."""
        print("Opening All Events Window")  # Debugging output
        self.all_events = AllEventsDisplay(self)  # Load all events UI
        self.all_events.show()  # Display window

    def on_signup(self, event, event_type):
        """Opens the sign-up window for the user to sign up for the associated event."""
        self.sign_up = EventSignUp(self, event, event_type)  # Load event sign-up UI
        self.sign_up.show()  # Display window

    def add_to_cart(self, item):
        """Adds an item to the cart in menu.py."""
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
