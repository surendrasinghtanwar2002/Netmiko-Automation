## Connection Type Menu Class ##
from .main_menu import Main_Menu
from typing import List
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
    def __netmiko_connection(self, device) -> object:
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
        """
        Threading Module method is being used to create multiple thread for multiple connection
        Attributes:- 
                     (1) device_deatils = List
        """
        try:
            with ThreadPoolExecutor(max_workers=5) as executor:
                self.netmiko_devices_connection = list(executor.map(self.__netmiko_connection, device_details))
                return self.netmiko_devices_connection
        except Exception as e:
            self.common_text(
                primary_text=Text_File.exception_text["common_function_exception"],
                secondary_text=str(e),
                secondary_text_color="red"
            )

    def __filter_method(self,device) -> bool:
        return "host" in device
    
    def __host_validation(self,Host_details:List,Filtered_Host:List):
        """
        Host Validation Method is the method to filtered those host which is responding back to our pind command
        Attributes:-
                     (1)Host_details = List
                     (2)Filtered_Host = List
        """
        self.valid_host = [ ]
        try:
            for host in Host_details:
                for filteredhost in Filtered_Host:
                    if host["host"] == filteredhost:
                        self.valid_host.append(host)
                    else:
                        pass
            return self.valid_host
        except Exception as e:
            self.common_text(primary_text=Text_File.exception_text["common_function_exception"],secondary_text=e,secondary_text_style="bold")

    ## Multiple device connection method
    def __multiple_device_connection(self):
        try:
            # Show progress bar before moving to the next screen
            result = self.progress_bar(Progessbar_name="Loading your Next Screen")
            
            if result:
                # Get device details (expected to be a list of dictionaries with 'host' key)
                device_details = self._multiple_device_auth_data()

                # Filter out devices that have the 'host' key
                filtered_devices = filter(self.__filter_method, device_details)
                ip_addresses = [device["host"] for device in filtered_devices]  # Extract IP addresses

                # Validate the extracted IP addresses
                valid_ip_address = self.ip_address_validation(ip_address=ip_addresses)

                # User input for printing the IP table
                user_choice = input(self.common_text(primary_text=Text_File.common_text["print_ip_table"])).strip()

                # If user chooses to print the IP table
                if user_choice.lower() == "yes":
                    # Display the table of valid IP addresses
                    self.Table_View_Output(
                        table_header=["Sequence", "IP Address"], 
                        table_data=valid_ip_address, 
                        user_Sequence=True
                    )
                # Validate the hosts that respond back to our ping command
                valid_host = self.__host_validation(
                    Host_details=device_details, 
                    Filtered_Host=valid_ip_address
                )
                # Start the threading module to handle connections concurrently
                result = self.__threading_module(device_details=valid_host)
                # Check if threading was successful
                if result:
                    # Push the established Netmiko connections to the global state manager
                    Global_State_Manager.Netmiko_State_Push_Manager(device=self.netmiko_devices_connection)
                    # Delay for 2 seconds to allow the next steps
                    self.sleep(time=2)
                    self.next_screen()
                else:
                    # Handle connectivity issue
                    self.common_text(
                        primary_text=Text_File.error_text["Connectivity_Issue"], 
                        secondary_text="Error during device connection", 
                        secondary_text_style="bold"
                    )
                    self.sleep(time=2)
                    self.exit_menu()

            # Handle when the progress bar result is False (or no next screen)
            else:
                self.common_text(primary_text="Progress bar failed or was canceled.", secondary_text_style="bold")

        except Exception as e:
            # Catch any exception and handle gracefully
            self.common_text(
                primary_text=Text_File.error_text["Connectivity_Issue"], 
                secondary_text=str(e), 
                secondary_text_style="bold"
            )
            self.sleep(time=2)
            self.exit_menu()

    ## Back to main menu method
    def back_to_main_menu(self):
        try:
            super().display_main_menu()                 ##Need to test that its working or not
        except Exception as e:
            print(f'Function: {__name__}, Exception: {type(e).__name__}')

