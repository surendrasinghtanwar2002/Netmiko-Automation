## Connection Type Menu Class ##
from .main_menu import Main_Menu
from typing import List
from automation.authentication.common_authentication import Authentication
from automation.components.common_decorator.common_decorator import NetmikoException_Handler,Regular_Exception_Handler,ThreadPoolExeceptionHandler
from netmiko import ConnectHandler
from assets.text_file import Text_File
from state.global_State_Manger import Global_State_Manager
from concurrent.futures import ThreadPoolExecutor
import sys

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

    @Regular_Exception_Handler
    def next_screen(self,connectiontype:object | List[object])->None:      
        """
        Displays the script menu based on the selected connection type.

        This method overrides the original `next_screen` method. It imports the `Script_Menu` 
        class and creates an instance of it, then calls its `display_main_menu()` method, 
        passing the specified `connectiontype`.

        Args:
            connectiontype (object | List[object]): The connection type or types to be used in the 
            script menu display.

        Returns:
            None
        """    
        from .script_menu import Script_Menu
        next__display = Script_Menu()
        next__display.display_main_menu(netmiko_type=connectiontype)

    @NetmikoException_Handler
    def __single_device_connection(self):
        """
        Establishes a connection to a single network device and updates the global state.

        This method displays a loading screen and prompts the user to authenticate 
        for a single device connection. It retrieves authentication data, establishes 
        a connection using Netmiko's `ConnectHandler`, and updates the global state 
        manager with the connection. If successful, it navigates to the next screen; 
        otherwise, it displays error messages.

        Returns:
            None
        """
        result = self.progress_bar(Progessbar_name=Text_File.common_text["Loading_Screen"])
        if result:
            self.clear_screen()
            self.common_text(primary_text=Text_File.common_text["Single_device"],primary_text_color="red", primary_text_style="bold")
            auth_data = self._single_device_auth_data()
            if auth_data:
                connection = ConnectHandler(**auth_data)
                if connection:
                    result = Global_State_Manager.Netmiko_State_Push_Manager(device=connection)
                    if result:
                        self.common_text(primary_text=Text_File.common_text["successful_state_update"], 
                                                    primary_text_color="green")
                        self.next_screen(connectiontype=connection)  # Passing Netmiko connection object
                    else:
                        self.common_text(secondary_text=Text_File.error_text["Device invalid"])
                else:
                     sys.exit(self.ExceptionTextFormatter(primary_text=Text_File.error_text["Connectivity_Issue"],add_line_break=False))
            else:
                 sys.exit(self.ExceptionTextFormatter(primary_text=Text_File.error_text["User_Auth_Data_error"],add_line_break=False))
        else:
            sys.exit(self.ExceptionTextFormatter(primary_text=Text_File.error_text["Error_in_script"],add_line_break=False))


    @NetmikoException_Handler
    def __netmiko_connection(self, device) -> object:
        """
        Establishes a Netmiko connection to a specified network device.

        This method attempts to create a connection to the provided device using 
        Netmiko's `ConnectHandler`. It displays the device's host information 
        and connection details. If the connection is successful, it returns the 
        connection object; otherwise, it displays an error message indicating the 
        failure.

        Args:
            device (dict): A dictionary containing device connection parameters, 
            such as host, username, and password.

        Returns:
            object: The established connection object if successful; 
            otherwise, returns None.
        """

        with ConnectHandler(**device) as connection:
            self.common_text(primary_text=device["host"],primary_text_color="yellow",primary_text_style="bold")
            self.common_text(primary_text=Text_File.common_text["Device_connection_details"],primary_text_color="yellow",primary_text_style="bold",secondary_text=device["host"])
            return connection

    @ThreadPoolExeceptionHandler
    def __threading_module(self,device_details:list) -> bool:
        """
        Creates multiple threads to establish connections to multiple network devices.

        This method utilizes a `ThreadPoolExecutor` to concurrently connect to a list 
        of network devices using the `__netmiko_connection` method. It returns a list 
        of connection objects if successful.

        Args:
            device_details (list): A list of dictionaries, each containing connection 
            parameters for a network device.

        Returns:
            bool: Returns True if connections are successfully established; 
            otherwise, returns False after displaying an error message.
        """
        with ThreadPoolExecutor(max_workers=5) as executor:
            self.netmiko_devices_connection = list(executor.map(self.__netmiko_connection, device_details))
            return self.netmiko_devices_connection

    @Regular_Exception_Handler
    def __filter_method(self,device) -> bool:
        """
        Checks if the device has a 'host' key.

        Args:
            device (dict): Device details.

        Returns:
            bool: True if 'host' exists, otherwise False.
        """
        return "host" in device

    @Regular_Exception_Handler
    def __host_validation(self,Host_details:List,Filtered_Host:List):
        """
        Validates hosts by filtering those that respond to a ping command.

        This method compares a list of host details against a list of filtered hosts 
        (those that are responding). It populates and returns a list of valid hosts 
        based on this comparison.

        Args:
            Host_details (List): A list of dictionaries containing details of all hosts.
            Filtered_Host (List): A list of host identifiers that responded to the ping command.

        Returns:
            List: A list of valid hosts that match the filtered hosts.
        """
        self.valid_host = [ ]
        for host in Host_details:
            for filteredhost in Filtered_Host:
                if host["host"] == filteredhost:
                    self.valid_host.append(host)
                else:
                    pass
        return self.valid_host


    @Regular_Exception_Handler
    def __multiple_device_connection(self):
        """
        Connect to multiple devices based on user authentication data, 
        validate IP addresses, and display connection results.
        
        Prompts the user to print the IP address table and handles 
        connectivity issues.
        """
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
            self.clear_screen()
            user_choice = input(
                self.common_text(
                    primary_text=Text_File.common_text["print_ip_table"],
                    primary_text_color="yellow",
                    primary_text_style="bold",
                    add_line_break=False
                )
            ).strip()
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
                    state_result = Global_State_Manager.Netmiko_State_Push_Manager(device=self.netmiko_devices_connection)
                    if state_result:
                        self.common_text(
                            primary_text=Text_File.common_text["successful_state_update"],
                            primary_text_color="yellow",
                            primary_text_style="bold"
                        )
                    # Delay for 2 seconds to allow the next steps
                    self.sleep(time=2)
                    self.next_screen(connectiontype=self.netmiko_devices_connection)  # Passing Netmiko connection object list prop
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
                self.common_text(primary_text="progress_bar_failed", secondary_text_style="bold")


    ## Back to main menu method
    def back_to_main_menu(self):
        try:
            super().display_main_menu()                 ##Need to test that its working or not
        except Exception as e:
            print(f'Function: {__name__}, Exception: {type(e).__name__}')

