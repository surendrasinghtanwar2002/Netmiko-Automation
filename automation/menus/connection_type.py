##Required modules
from automation.device_connection.device_connection import Device_Connection
from assets.text_file import Text_File
from automation.authentication.authentication import single_device_auth,multiple_device_auth
from automation.menus.script_menu import ScriptMenu
class ConnectionTypeMenu:
    def __init__(self,menu_utils) -> None:
        self.menu_utils = menu_utils
        self.script_action = {
            "1": self.single_device_connection,
            "2": self.multiple_device_connection,
            "3": self.back_to_main_menu,
            "4": self.default_action
        }
        self.menu_items = ["Single Device Connection", "Multiple Device Connection", "Back to Main Menu"]

    ##Handler for back_to_main_menu
    def back_to_main_menu(self) -> None:
        print("Navigating to Main Menu...")
        from automation.menus.main_menu import MainMenu             ##Delay Factor
        main_menu = MainMenu(self.menu_utils)               
        main_menu.display()

    ##Handler for script menu
    @staticmethod           ##This is the static method
    def navigating_script_menu(self)->None:
        print("Navigation to script menu.....")
        script_navigation = ScriptMenu(self.menu_utils)
        script_navigation.script_display_menu()


    def single_device_connection(self):
        username, userpass, hostipaddress = single_device_auth()
        try:
            connection = Device_Connection(username, userpass, hostipaddress)
            netmiko_connection = connection.single_device_connection()
            if netmiko_connection:
                self.navigating_script_menu()  # Pass the connection here
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
            result = self.navigating_script_menu(netmiko_connection) 
            if result:
                print("We have got the result")         ##This is the 
        else:
            print(Text_File.error_text["device_details_error"])
        return True

    def default_action(self):
        return False

    def connection_display_menu(self):
        while True:
            self.menu_utils.display_menu(self.menu_items)
            user_choice = self.menu_utils.get_user_choice(self.script_action)
            if self.script_action.get(user_choice)():
                break