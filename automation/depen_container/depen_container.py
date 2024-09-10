# automation/di_container.py
from automation.menus.main_menu import MainMenu
from automation.menus.script_menu import ScriptMenu
from automation.menus.connection_type import ConnectionTypeMenu
from automation.menus.menu_utils import MenuUtils

##Container for the 
class DIContainer:
    def __init__(self):
        self.menu_utils = MenuUtils()           ##This is menu utils class contain the (Display function & User choice Function) 
        self.connection_menu = ConnectionTypeMenu(self.menu_utils)
        self.script_menu = ScriptMenu(self.menu_utils)
        self.main_menu = MainMenu(self.menu_utils)
        
    def get_main_menu(self):
        self.connection_menu.main_menu = self.main_menu
        return self.main_menu