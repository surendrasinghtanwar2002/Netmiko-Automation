                                                ## Main Class Definition ##
##Importing required Modules
import sys 
sys.path.append('/Users/surendrasingh/Desktop/NETWORKING_AUTOMATION/menus')
from connection_type_menu import Connection_Type_Menu

class Main_Menu:
    def __init__(self) -> None:
        self.connection_menu = Connection_Type_Menu(self)
        self.script_action = {
            "1": self.handle_cisco,
            "2": self.handle_juniper,
            "3": self.handle_arista,
            "4": self.handle_dell,
            "5": self.default_action
        }
        self.menu_item = ["Cisco", "Juniper", "Arista", "Dell"]

    # Define specific functions for each selection
    def handle_cisco(self):
        print("Handling Cisco script execution.")
        self.connection_menu.connection_display_menu()
        return True

    def handle_juniper(self):
        print("Handling Juniper script execution.")
        self.connection_menu.connection_display_menu()
        return True

    def handle_arista(self):
        print("Handling Arista script execution.")
        self.connection_menu.connection_display_menu()
        return True

    def handle_dell(self):
        print("Handling Dell script execution.")
        self.connection_menu.connection_display_menu()

    # Default action if selection is not found (optional)
    def default_action(self):
        print("Invalid selection, please try again.")
        return True

    # Display Menu
    def main_menu_display(self):
        while True:
            from menu_utils import display_menu, get_user_choice
            display_menu(self.menu_item)    ##priting the display
            user_choice = get_user_choice(self.script_action)
            if self.script_action[user_choice]():
                break

if __name__ == "__main__":
    main_menu = Main_Menu()  # Creates an instance of Main_Menu
    main_menu.display_menu()
