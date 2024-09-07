from automation.menus.menu_utils import MenuUtils
from automation.menus.main_menu import MainMenu, ScriptMenu, ConnectionTypeMenu

def main():
    menu_utils = MenuUtils()
    script_menu = ScriptMenu(menu_utils=menu_utils)
    connection_menu = ConnectionTypeMenu(main_menu_instance=None, script=script_menu, menu_utils=menu_utils) 
    main_menu = MainMenu(menu_utils=menu_utils, connection_menu=connection_menu)
    connection_menu.main_menu_instance = main_menu
    main_menu.display()

if __name__ == "__main__":
    main()
