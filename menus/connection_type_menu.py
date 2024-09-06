import sys
sys.path.append('/Users/surendrasingh/Desktop/NETWORKING_AUTOMATION/menus')
from scripts_menu import ScriptMenu

class Connection_Type_Menu:
    ##creating the script menu object
    procedure = ScriptMenu()
    def __init__(self,main_menu_instance) -> None:
        self.main_menu_instance = main_menu_instance
        # self.ScriptMenu = ScriptMenu(self)
        self.script_action = {
            "1": self.single_device_connection,
            "2": self.multiple_device_connection,
            "3": self.back_to_main_menu,
            "4": self.default_action
        }
        self.menu_item = ["Single Device Connection", "Multiple Device Connection", "Back to Main Menu"]

    def single_device_connection(self):
        self.procedure.script_display_menu()
        return True

    def multiple_device_connection(self):
        self.procedure.script_display_menu()
        return True

    def back_to_main_menu(self):
        self.main_menu_instance.main_menu_display()
        return False

    def default_action(self):
        return False

    def connection_display_menu(self):
        from menu_utils import display_menu, get_user_choice
        while True:
            display_menu(self.menu_item)
            user_choice = get_user_choice(self.script_action)
            if self.script_action[user_choice]():
                break
