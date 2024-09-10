from automation.menus.connection_type import ConnectionTypeMenu
## Main Menu Class
class MainMenu:
    def __init__(self, menu_utils) -> None:
        self.menu_utils = menu_utils
        self.script_action = {
            "1": self.handle_cisco,
            "2": self.handle_juniper,
            "3": self.handle_arista,
            "4": self.handle_dell,
            "5": self.default_action
        }
        self.menu_items = ["Cisco", "Juniper", "Arista", "Dell"]      

    ##Handler for managing the navigation
    def go_to_connection_menu(self) -> None:
        print("Navigating to Connection Menu...")
        connection_menu = ConnectionTypeMenu(self.menu_utils)
        connection_menu.connection_display_menu()

    # Define specific functions for each selection
    def handle_cisco(self)->None:
        print("Handling Cisco script execution.")   
        self.go_to_connection_menu()
        return True

    def handle_juniper(self)->None:
        print("Handling Juniper script execution.")     
        self.go_to_connection_menu()
        return True

    def handle_arista(self)->None:
        print("Handling Arista script execution.")     
        self.go_to_connection_menu()
        return True

    def handle_dell(self)->None:
        print("Handling Dell script execution.")        
        self.go_to_connection_menu()
        return True

    # Default action if selection is not found (optional)
    def default_action(self)->None:
        print("Invalid selection, please try again.")  
        return True

    # Display Menu  
    def display(self)->None:
        while True:
            self.menu_utils.display_menu(self.menu_items)
            choice = self.menu_utils.get_user_choice(self.script_action)
            if self.script_action.get(choice)():
                break