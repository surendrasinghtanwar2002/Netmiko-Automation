## Importing required Modules
import os
import importlib.util
from automation.menus.menu_utils import MenuUtils
from automation.device_connection.device_connection import Device_Connection
from assets.text_file import Text_File
from automation.authentication.authentication import single_device_auth,multiple_device_auth,clear
## Main Menu Class
class MainMenu:
    def __init__(self, menu_utils: MenuUtils, connection_menu: 'ConnectionTypeMenu') -> None:
        self.menu_utils = menu_utils
        self.connection_menu = connection_menu
        self.script_action = {
            "1": self.handle_cisco,
            "2": self.handle_juniper,
            "3": self.handle_arista,
            "4": self.handle_dell,
            "5": self.default_action
        }
        self.menu_items = ["Cisco", "Juniper", "Arista", "Dell"]

    # Define specific functions for each selection
    def handle_cisco(self)->None:
        print("Handling Cisco script execution.")   ##Debug
        self.connection_menu.connection_display_menu()
        return True

    def handle_juniper(self)->None:
        print("Handling Juniper script execution.")     ##Debug
        self.connection_menu.connection_display_menu()
        return True

    def handle_arista(self)->None:
        print("Handling Arista script execution.")      ##Debug
        self.connection_menu.connection_display_menu()
        return True

    def handle_dell(self)->None:
        print("Handling Dell script execution.")        ##Debug
        self.connection_menu.connection_display_menu()
        return True

    # Default action if selection is not found (optional)
    def default_action(self)->None:
        print("Invalid selection, please try again.")   ##Debug
        return True

    # Display Menu  
    def display(self)->None:
        while True:
            self.menu_utils.display_menu(self.menu_items)
            choice = self.menu_utils.get_user_choice(self.script_action)
            if self.script_action.get(choice)():
                break

## Script Menu Class
class ScriptMenu:
    def __init__(self, menu_utils) -> None:
        self.menu_utils = menu_utils
        self.script_action = self.load_script_actions()
        self.menu_items = self.menu_items_list()

    def menu_items_list(self) -> list:
        path = "/Users/surendrasingh/Desktop/Netmiko-Automation/automation/scripts/cisco_script"
        exclude_items = {"__init__.py", "unwanted_file.py", "__pycache__"}
        dir_list = [item.strip(".py") for item in os.listdir(path) if item not in exclude_items]
        print(f"Menu items: {dir_list}")  # Debugging statement
        return dir_list

    def load_script_actions(self) -> dict:
        menu_items = self.menu_items_list()
        items_sequence = len(menu_items)
        print(f"Menu items for actions: {menu_items}")  # Debugging statement
        return {str(i + 1): self.create_script_action(menu_items[i]) for i in range(items_sequence)}

    def create_script_action(self, script_name: str):
        def action(*args, **kwargs):
            module = self.import_module(script_name)
            if module:
                func = getattr(module, 'main', None)
                if func and callable(func):
                    try:
                        result = func(*args, **kwargs)
                        return result
                    except TypeError as e:
                        print(f"Error calling {script_name}.main with args={args} kwargs={kwargs}: {e}")
                else:
                    print(f"Function `main` not found in {script_name}")
                    return None
            return False
        return action

    def import_module(self, script_name: str):
        path = "/Users/surendrasingh/Desktop/Netmiko-Automation/automation/scripts/cisco_script"
        module_path = os.path.join(path, f"{script_name}.py")
        if not os.path.isfile(module_path):
            print(f"Module {script_name} does not exist.")
            return None
        spec = importlib.util.spec_from_file_location(script_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def script_display_menu(self, connection):  # Accept connection as parameter
        while True:
            self.menu_utils.display_menu(self.menu_items)
            user_choice = self.menu_utils.get_user_choice(self.script_action)
            action = self.script_action.get(user_choice)            ##Dynamically generate function object
            if action:
                result = action(connection)  # Pass the connection to the action and get the result
                if result is True:
                    break
                elif result is not None:
                    print(f"Result from script: {result}") 
        return result  # Return the final result


## Connection Type Class
class ConnectionTypeMenu:
    def __init__(self, main_menu_instance: MainMenu, script: ScriptMenu, menu_utils: MenuUtils) -> None:
        self.main_menu_instance = main_menu_instance
        self.procedure = script
        self.menu_utils = menu_utils
        self.script_action = {
            "1": self.single_device_connection,
            "2": self.multiple_device_connection,
            "3": self.back_to_main_menu,
            "4": self.default_action
        }
        self.menu_items = ["Single Device Connection", "Multiple Device Connection", "Back to Main Menu"]

    def single_device_connection(self):
        username, userpass, hostipaddress = single_device_auth()
        try:
            connection = Device_Connection(username, userpass, hostipaddress)
            netmiko_connection = connection.single_device_connection()
            if netmiko_connection:
                self.procedure.script_display_menu(netmiko_connection)  # Pass the connection here
            else:
                print(Text_File.error_text["device_details_error"])
            return True
        
        except ValueError as value:
            print(f"{Text_File.exception_text['value_error']} {value}")
        
        except Exception as e:
            print(f"{Text_File.exception_text['common_function_exception']}",e)

    def multiple_device_connection(self):
        username, userpass, hostipaddress = multiple_device_auth()
        connection = Device_Connection(username, userpass, hostipaddress)
        netmiko_connection = connection.multiple_device_connection()  # Fixed method name
        if netmiko_connection:
            result = self.procedure.script_display_menu(netmiko_connection)  
            if result:
                print("We have got the result")         ##This is the 
        else:
            print(Text_File.error_text["device_details_error"])
        return True

    def back_to_main_menu(self):
        self.main_menu_instance.display()  # Call to MainMenu.display()
        return False

    def default_action(self):
        return False

    def connection_display_menu(self):
        while True:
            self.menu_utils.display_menu(self.menu_items)
            user_choice = self.menu_utils.get_user_choice(self.script_action)
            if self.script_action.get(user_choice)():
                break

# Example Usage
if __name__ == "__main__":
    menu_utils = MenuUtils()  
    script_menu = ScriptMenu(menu_utils=menu_utils)  
    main_menu = MainMenu(menu_utils=menu_utils, connection_menu=None)  
    connection_menu = ConnectionTypeMenu(main_menu_instance=main_menu, script=script_menu, menu_utils=menu_utils)

    main_menu.connection_menu = connection_menu

    main_menu.display()
