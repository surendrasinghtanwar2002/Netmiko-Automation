import json
from assets.text_file import Text_File
from assets.text_style import Text_Style
from concurrent.futures import ThreadPoolExecutor
from tabulate import tabulate
import re
class Common_Methods(Text_Style):
    def __init__(self,netmiko_connection:object) -> None:
        self.netmiko_connection = netmiko_connection
    
    def configuration_menu(self,menu_items:list)->None:
        """
        The method configuration menu is used to display the configuration menu items on the screen \n
        Arguments:- 
                    (1) menu_items -> List
        """
        try:
            for item_no,item_value in enumerate(menu_items,start=1):
                self.common_text(primary_text=f"({item_no}) {item_value}")
        except ValueError as value:
            self.common_text(primary_text=Text_File.exception_text["value_error"],secondary_text=value)
            return False
        except Exception as e:
            self.common_text(primary_text=Text_File.exception_text["common_function_exception"],secondary_text=f"{__name__} {e}")
            return False

    def Interface_details(self, interface_details:dict)->None:
        """
        The method Interface details is used to display the details of device interface \n
        Arguments:- 
                    (1)interface_details -> dict
        """
        try:
            user_input = input(self.common_text(primary_text=Text_File.common_text["interface_details"])).strip().lower()
            if user_input == "yes":
                self.common_text(primary_text=Text_File.common_text["show_interface_details"],primary_text_color="yellow",secondary_text=f"\n{interface_details}",secondary_text_color="green")
                return interface_details
        except Exception as e:
            self.common_text(primary_text=Text_File.exception_text["common_function_exception"],secondary_text=e)
            return False
        
    def Data_convertor(self,raw_data:str,indentation:int=4)->object | str:
        """
        The method Json_String_Convertor is used to convert the raw data into Json data \n
        Arguments:-
                    (1) raw_Data -> str
                    (2) indentation -> int
        """
        menu_items = ["Json String to a Python object","Python object to a Json String","Exit"]
        try:
            self.configuration_menu(menu_items=menu_items)
            counter_value = 1
            max_value = 3
            while counter_value < max_value:
                user_choice =input(self.common_text(primary_text=Text_File.common_text["user_choice_no"])).strip()
                match user_choice:
                    case 1:                 ##JSON String to Python object
                        self.common_text(primary_text=Text_File.common_text["json_to_python_object"],primary_text_color="yellow")
                        if isinstance(raw_data,str):
                            python_object = json.loads(raw_data)
                            return python_object
                        else:
                            counter_value += 1          #-> Increasing counter by 1
                            self.common_text(primary_text=Text_File.error_text["json_to_python_object_error"])
                    case 2:                 ##Python object to Json String
                        self.common_text(primary_text=Text_File.common_text["object_to_json_string"])
                        if isinstance(raw_data,dict):
                            json_string = json.dumps(raw_data,indent=indentation)
                            return json_string
                        else:
                            counter_value += 1          #->Increasing counter by 1
                            self.common_text(primary_text=Text_File.error_text["Python_object_to_json_error"])
                    case 3:
                        return False;
                    case _:
                        self.common_text(primary_text=Text_File.common_text["valid_option_warn"])
        except Exception as e:
            self.common_text(primary_text=Text_File.exception_text["common_function_exception"],secondary_text=f"{__name__,e}")

    def Interface_validation(self, interface_name: str | list, interface_detail_data: dict)->bool:
        """
        The method Interface validation is used to validate the interface from the device data.\n
        Arguments:-
                    (1) interface_name -> str
                    (2) interface_detail_data -> dict
        """
        valid_interface = []  # This will hold valid interface names
        try:
            # Check if interface_name is a string
            if isinstance(interface_name, str):
                # Use next to find the first matching interface
                interface_confirmation = next(
                    (item for item in interface_detail_data if item["interface"] == interface_name), 
                    None
                )
                return interface_confirmation if interface_confirmation else False

            # Check if interface_name is a list
            elif isinstance(interface_name, list):
                # Loop through the interface_detail_data and interface_name
                for item in interface_detail_data:
                    if item["interface"] in interface_name:
                        valid_interface.append(item["interface"])  # Add valid interface to the list
                
                return valid_interface

        except Exception as e:
            print(f"This is the exception of the function: {e}")

    def getTableViewInterfaceDetails(self,interface_details:dict)->None:
        """
        The method getTableViewInterfaceDetails is used to print the interface details in table format.\n
        Arguments:- 
                    (1) interface_details = dict
        """
        try:
            header = ["Interface Name","Ip Address","Status","Prototype"]
            table_data = []
            for data in interface_details:
                row = [data.get("interface"),
                    data.get("ip_address"),
                    data.get("status"),
                    data.get("proto")
                    ]
                table_data.append(row)
            ##display the items
            self.common_text(primary_text=f"{tabulate(table_data, header, tablefmt="heavy_grid")}",primary_text_color="yellow")

        except Exception as e:
            self.common_text(primary_text=Text_File.exception_text["common_function_exception"],secondary_text=f"{__name__,e}")
            return False

    def patternExplorer(self,Pattern:str,Raw_Data:str):
        """
        Find the pattern from the raw data

        Args:
             Pattern (string): The Pattern to apply on the data
             Raw_Data (string): The data where regex pattern will be applied
        """
        try:
            result = re.search(Pattern,Raw_Data)
            if result:
                user_choice = input(f"{result} [Yes/No]:- ").strip().lower()
                Raw_Data += self.netmiko_connection.send_command(user_choice)
                return Raw_Data
            else:
                return Raw_Data

        except Exception as e:
            print("In this exception occurs of the function",e)


            #######################################***&&&&&****((((((((((((((((We need to work from here because paralle device commands is still not working properly))))))))))))))))
    def parallelDeviceCommand(self, device_list: list, command_list: str | list, configuration: bool = False):
            """
            Sends commands or a list of commands in parallel to a list of devices
            and waits for a user prompt if one is available.

            Args:
                device_list: List of Netmiko Device connection objects
                command_list: A string command or a list of commands to pass to multiple devices
                configuration: Whether the commands are configuration commands (default is False)
            """
            try:
                
                if isinstance(command_list, str):
                    command_list = [command_list] * len(device_list)  # Duplicate for each device
                elif isinstance(command_list, list):
                    command_list = command_list * len(device_list)  # Duplicate the list

                # Create a list of devices corresponding to the command list
                devices = [device for device in device_list for _ in range(len(command_list) // len(device_list))]

                # Execute commands in parallel
                with ThreadPoolExecutor(max_workers=5) as executor:
                    output = list(executor.map(self.commands_send, command_list, [configuration] * len(command_list), devices))
                return output

            except Exception as e:
                print(f"This is the exception of the function: {e}")
                return []

   def commands_send(self, command: str | list, configuration: bool = False, device=None):
    """
    Sends a command to a single device.

    Args:
        command (str | list): The command(s) to be sent (string or list of strings).
        configuration (bool): Whether the command is a configuration command.
        device: The device connection object to send the command to.
    """
    user_pattern = r"^(.*?\[confirm\].*?|.*?\?.*?)$"  # Regex pattern for user prompts
    final_output = ""

    try:
        if isinstance(device, object):  # Ensure device is a valid object
            if isinstance(command, str):
                output = device.send_config_set(command) if configuration else device.send_command_timing(command)
                result = self.patternExplorer(Pattern=user_pattern, Raw_Data=output)
                final_output += f"----------- Host {device.host} -----------\n{result if result else output}"
                return final_output

            elif isinstance(command, list):
                for cmd in command:
                    output = device.send_config_set(cmd) if configuration else device.send_command_timing(cmd)
                    result = self.patternExplorer(Pattern=user_pattern, Raw_Data=output)
                    final_output += f"----------- Host {device.host} -----------\n{result if result else output}"
                return final_output

        else:
            print("Invalid device input")
            return False

    except Exception as e:
        print(f"Exception in commands_send function: {e}")
        return ""


