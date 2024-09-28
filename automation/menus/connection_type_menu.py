## Connection Type Menu Class ##
from .main_menu import Main_Menu
from netmiko import ConnectHandler
from assets.text_file import Text_File
from maskpass import advpass, askpass
from .Multiple_device_connection import MultipleDeviceConnection
import platform
import subprocess
import shutil
import os

class Connection_type_menu(Main_Menu,MultipleDeviceConnection):
    device_type = "cisco_ios"  ##Class Attributes
    netmiko_connection = None

    def __init__(self) -> None:
        connectiontype_menu_items = ["Single Device Connection", "Multiple Device Connection", "Back to Main Menu", "Exit Menu"]  ## Constructor for the class
        connection_type_event_handlers = { 
            "1": self.single_device_connection,
            "2": self.multiple_device_connection,
            "3": self.back_to_main_menu,
            "4": self.exit_menu
        }
        super().__init__(menu_items=connectiontype_menu_items, event_handlers=connection_type_event_handlers)

    ## IP address validation for single device and multiple devices
    @staticmethod                   
    def __ip_address_validation(ip_address: None):
        param = '-n' if platform.system().lower() == 'win32' else '-c'
        valid_ip_addresses = []  ## valid IP address list 
        try:
            if isinstance(ip_address, str):
                host = ip_address
                command = ["ping", param, "2", host]
                if subprocess.call(command) == 0:
                    return True
                else:
                    return False
            elif isinstance(ip_address, list):
                print("Multiple IP Address Pinging Method")  ## Debug purpose
                for ip in ip_address:
                    host = ip
                    command = ["ping", param, "2", host]
                    if subprocess.call(command) == 0:
                        valid_ip_addresses.append(ip)  ## Append valid IP addresses
                    else:
                        print(f"IP Address is not valid: {ip}")
                return valid_ip_addresses
        except subprocess.CalledProcessError as processerror:
            print(f'Function: {__name__}, Exception: {type(processerror).__name__}')

    @classmethod  ## Use this when we need to change the device type
    def device_type_details(cls, device_new_type):
        try:
            cls.device_type = device_new_type
            return cls.device_type
        except Exception as e:
            print(f'Function: {__name__}, Exception: {type(e).__name__}')

    @classmethod  ## Class method for initializing the Netmiko object globally
    def netmiko_connection_initializer(cls, new_netmiko_connection: object) -> object:
        try:
            cls.netmiko_connection = new_netmiko_connection              
            return cls.netmiko_connection
        except Exception as e:
            print(f'Function: {__name__}, Exception: {type(e).__name__}')

    ## Single device authentication connection
    @Main_Menu._timeexecution
    def __single_device_auth_connection(self) -> tuple[str, str, str]:
        try:
            counter_start = 0
            counter_end = 3
            while counter_start < counter_end:
                user_ip_address = input("Enter your IP Address: ")
                result = self.__ip_address_validation(user_ip_address)
                if result:
                    self._clear_screen()
                    print(f"Your IP Address is Up {user_ip_address}".center(shutil.get_terminal_size().columns))  
                    user_name = input("Enter Username: ").strip()
                    user_pass = advpass() if os.name == "nt" else askpass()
                    if user_name and user_pass:
                        return (user_name, user_pass, user_ip_address)
                    else:
                        print(f"!!! You have passed one or both details empty !!!")
                        counter_start += 1
                else:
                    self._clear_screen()
                    print(f"Your IP Address is not up. Please check it again: {user_ip_address}".center(shutil.get_terminal_size().columns, "!"))
            print("!!! You have reached your limit !!!")
            return ("", "", "")
        except ValueError as value:
            print(f'Function: {__name__}, Exception: {type(value).__name__}')
        except Exception as e:
            print(f'Function: {__name__}, Exception: {type(e).__name__}')

    @Main_Menu._timeexecution
    def device_details_converter(self, device_details):
        return {
            "device_type": self.__class__.device_type,  ## Access class attribute properly
            "host": device_details[2],
            "username": device_details[0],
            "password": device_details[1]
        }
    @staticmethod
    @Main_Menu._timeexecution  
    def __next_screen()->None:
        from script_menu import Script_Menu
        next__display = Script_Menu()
        next__display.display_main_menu()

    ## Single device connection method
    @Main_Menu._timeexecution
    def single_device_connection(self):
        try:
            result = self.progress_bar(Progessbar_name="Loading your Next Screen")
            if result:
                self._clear_screen()
                self.common_text(primary_text=Text_File.common_text["Single_device"],primary_text_color="green")
                auth_data = self.__single_device_auth_connection()
                if auth_data == ("", "", ""):
                    self.common_text(primary_text=Text_File.common_text["invalid_credentials"],primary_text_color="red")
                    return 
   
                device_details = self.device_details_converter(device_details=auth_data)
                netmiko_connection = ConnectHandler(**device_details)
                if netmiko_connection:
                    self.netmiko_connection_initializer(new_netmiko_connection=netmiko_connection)  ## Class method to set netmiko object
                    print(netmiko_connection)
                    self.__next_screen()
                else:
                    print("We are not connected to the device")
        except Exception as e:
            print(f'Function: {__name__}, Exception: {type(e).__name__}')
    
    ## Multiple device connection method
    @Main_Menu._timeexecution
    def multiple_device_connection(self):
        try:
            self.Multiple_Host_connection()
        except Exception as e:
            print(f'Function: {__name__}, Exception: {type(e).__name__}')
    
    ## Back to main menu method
    @Main_Menu._timeexecution
    def back_to_main_menu(self):
        try:
            back = Main_Menu()
            back.display_main_menu()
        except Exception as e:
            print(f'Function: {__name__}, Exception: {type(e).__name__}')

## Creating the instance of connection type menu
def main():
    obj = Connection_type_menu()
    obj.display_main_menu()
    print(obj.netmiko_connection)

## Calling the main menu
if __name__ == "__main__":
    main()
