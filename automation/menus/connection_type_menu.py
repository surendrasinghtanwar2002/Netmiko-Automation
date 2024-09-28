## Connection Type Menu Class ##
from .main_menu import Main_Menu
from automation.authentication.common_authentication import Authentication
from netmiko import ConnectHandler
from assets.text_file import Text_File
from state.global_State_Manger import Global_State_Manager
from concurrent.futures import ThreadPoolExecutor


class Connection_type_menu(Main_Menu,Authentication):
    def __init__(self) -> None:
        self.netmiko_devices_connection = []  # A list to store the netmiko device connections
        self.connectiontype_menu_items = ["Single Device Connection", "Multiple Device Connection", "Back to Main Menu", "Exit Menu"]  ## Constructor for the class
        self.connection_type_event_handlers = { 
            "1": self.single_device_connection,
            "2": self.multiple_device_connection,
            "3": self.back_to_main_menu,
            "4": self.exit_menu
        }
        super().__init__(menu_items= self.connectiontype_menu_items, event_handlers=self.connection_type_event_handlers)
  
    @staticmethod
    def scriptmenu_next_screen()->None:
        try:
            from .script_menu import Script_Menu
            next__display = Script_Menu()
            next__display.display_main_menu()
        except Exception as e:
            print(f"Script menu next screen error {e}")

    ## Single device connection method
    def single_device_connection(self):
        try:
            result = self.progress_bar(Progessbar_name="Loading your Next Screen")
            if result:
                self._clear_screen()
                self.common_text(primary_text=Text_File.common_text["Single_device"],primary_text_color="red")
                auth_data = self._single_device_auth_data()
                print(f"--------------> This is the auth data of the function {auth_data} <----------------")           ##Debugger
                if auth_data:
                    print("You are data is proper we are sending to the server")                                        ##Debugger
                    netmiko_connection = ConnectHandler(**auth_data)
                    print(f"This is the netmiko connection  object -------------->{netmiko_connection} <--------------------")
                if netmiko_connection:
                    result = Global_State_Manager.Netmiko_State_Push_Manager(device=netmiko_connection)
                    if result:
                        print(f"Your data have been stored succesfully")
                        self.scriptmenu_next_screen()
                        
                # else:
                #     print("We are not connected to the device")
        except Exception as e:
            print(f'Function: {__name__}, Exception: {type(e).__name__}')

    ##Method for multiple device connection
    def netmiko_connection(self, device) -> object:
        try:
            with ConnectHandler(**device) as connection:
                print(f"Connected to {device['host']}")
                return connection
        except Exception as e:
            self.common_text(
                primary_text=Text_File.exception_text["connection_failed"],
                secondary_text=device['host'], 
                secondary_text_color="red"
            )

    def threading_module(self,device_details:list) -> bool:
        try:
            with ThreadPoolExecutor(max_workers=5) as executor:
                self.netmiko_devices_connection = list(executor.map(self.netmiko_connection, device_details))
                # Global_State_Manager.Netmiko_State_Push_Manager(device=self.netmiko_devices_connection)  # Add connections to global state manager
                return self.netmiko_devices_connection
        except Exception as e:
            self.common_text(
                primary_text=Text_File.exception_text["common_function_exception"],
                secondary_text=str(e),
                secondary_text_color="red"
            )
    @staticmethod
    def _filter_method(device) -> bool:
        return "host" in device
    
    ## Multiple device connection method
    def multiple_device_connection(self):
        try:
            result = self.progress_bar(Progessbar_name="Loading your Next Screen")
            if result:
                device_details = self._multiple_device_auth_data()                                              ##Return device details in list dictionary
                filtered_devices = filter(self._filter_method, device_details)  # Use filter to get devices with the 'host' key
                ip_addresses = [device["host"] for device in filtered_devices]  # Extracting IP addresses
                valid_ip_address = self._ip_address_validation(ip_address=ip_addresses)
                user_choice = input(self.common_text(primary_text=Text_File.common_text["print_ip_table"])).strip()
                if user_choice == "yes":
                    self.__printing_valid_ip_address_table(host_ip=valid_ip_address)
                    self.clear()
                    result = self.threading_module(device_details=device_details)
                    print(result)
                else:
                    pass
        except Exception as e:
            self.common_text(
                primary_text=Text_File.exception_text["common_function_exception"],
                secondary_text=str(e),
                secondary_text_color="red"
            )
    
    ## Back to main menu method
    def back_to_main_menu(self):
        try:
            back = Main_Menu()
            back.display_main_menu()
        except Exception as e:
            print(f'Function: {__name__}, Exception: {type(e).__name__}')

