## Connection Type Menu Class ##
from .main_menu import Main_Menu
from automation.authentication.common_authentication import Authentication
from netmiko import ConnectHandler
from assets.text_file import Text_File
from state.global_State_Manger import Global_State_Manager
from concurrent.futures import ThreadPoolExecutor


class Connection_type_menu(Main_Menu,Authentication):
    def __init__(self,menu_items=None, event_handlers=None) -> None:
        self.netmiko_devices_connection = []  # A list to store the netmiko device connections
        self.connectiontype_menu_items = menu_items if menu_items else ["Single Device Connection", "Multiple Device Connection", "Back to Main Menu", "Exit Menu"]  ## Constructor for the class
        self.connection_type_event_handlers = event_handlers if event_handlers else { 
            "1": self.__single_device_connection,
            "2": self.__multiple_device_connection,
            "3": self.back_to_main_menu,
            "4": self.exit_menu
        }
        super().__init__(menu_items=menu_items if menu_items else self.connectiontype_menu_items, 
                 event_handlers=event_handlers if event_handlers else self.connection_type_event_handlers)

    def next_screen(self)->None:            ##overide the original method
        try:
            from .script_menu import Script_Menu
            next__display = Script_Menu()
            next__display.display_main_menu()
        except Exception as e:
            self.common_text(primary_text=Text_File.common_text["common_function_exception"],secondary_text=e,secondary_text_style="bold")

    ## Single device connection method
    def __single_device_connection(self):
        try:
            result = self.progress_bar(Progessbar_name="Loading your Next Screen")
            if result:
                self.clear_screen()
                self.common_text(primary_text=Text_File.common_text["Single_device"],primary_text_color="red")
                auth_data = self._single_device_auth_data()
                if auth_data:
                    netmiko_connection = ConnectHandler(**auth_data)
                if netmiko_connection:
                    result = Global_State_Manager.Netmiko_State_Push_Manager(device=netmiko_connection)
                    if result:
                        self.common_text(primary_text=Text_File.common_text["successful_state_update"],primary_text_color="green")
                        self.next_screen()               ## Redirected to next screen ##              
                else:
                    self.common_text(secondary_text=Text_File.error_text["Device invalid"])
        except Exception as e:
            self.common_text(primary_text=Text_File.exception_text["common_function_exception"],secondary_text=e)

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

    def __threading_module(self,device_details:list) -> bool:
        try:
            with ThreadPoolExecutor(max_workers=5) as executor:
                self.netmiko_devices_connection = list(executor.map(self.netmiko_connection, device_details))
                Global_State_Manager.Netmiko_State_Push_Manager(device=self.netmiko_devices_connection)  # Add connections to global state manager
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
    def __multiple_device_connection(self):
        try:
            result = self.progress_bar(Progessbar_name="Loading your Next Screen")
            if result:
                device_details = self._multiple_device_auth_data()                                              ##Return device details in list dictionary
                filtered_devices = filter(self._filter_method, device_details)  # Use filter to get devices with the 'host' key
                ip_addresses = [device["host"] for device in filtered_devices]  # Extracting IP addresses
                valid_ip_address = self.ip_address_validation(ip_address=ip_addresses)
                user_choice = input(self.common_text(primary_text=Text_File.common_text["print_ip_table"])).strip()
                if user_choice == "yes":
                    self.clear_screen()
                    self.printing_valid_ip_address_table(host_ip=valid_ip_address)        ##also need to work here also
                    result = self.__threading_module(device_details=device_details)       ##Here we need to work that we need to filter those ip address which is not valid
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
            super().display_main_menu()                 ##Need to test that its working or not
        except Exception as e:
            print(f'Function: {__name__}, Exception: {type(e).__name__}')

