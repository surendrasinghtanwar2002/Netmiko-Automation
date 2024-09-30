from maskpass import askpass
from typing import Tuple, Union,Dict,List
from assets.text_file import Text_File
from assets.text_style import Text_Style
from tabulate import tabulate
from assets.text_file import Text_File
import shutil
import os
import platform
import subprocess
##clear screen function

##single_device_connection_auth
class Authentication(Text_Style):
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def clear_screen()->None:
       os.system('cls' if platform.system() == 'Windows' else 'clear')

    @staticmethod       
    def ip_address_validation(ip_address: str | list)->list:
        param = '-n' if platform.system().lower() == 'win32' else '-c'
        valid_ip_addresses = []  ## valid IP address list 
        try:
            if isinstance(ip_address, str):
                host = ip_address
                command = ["ping", param, "2", host]
                if subprocess.call(command) == 0:
                    return ip_address
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
            return []
        except subprocess.CalledProcessError as processerror:
            print(f'Function: {__name__}, Exception: {type(processerror).__name__}')
            return []
    
    def printing_valid_ip_address_table(self,host_ip:List[str])->None:         ##Method to print the valid ip address
        self.clear_screen()         ##Clear Screen Function
        table_data = []
        header = ["Sequence","Ip_Address"]
        for sequence,ip_address in enumerate(host_ip,start=1):
            table_data.append([sequence,ip_address])
        print(tabulate(table_data,header,tablefmt="double_outline").center(shutil.get_terminal_size().columns))

    def _single_device_auth_data(self) -> tuple[str, str, str]:
        try:
            counter_start = 0
            counter_end = 3

            while counter_start < counter_end:
                user_ip_address = input("Enter your IP Address: ")
                result = self.ip_address_validation(user_ip_address)
                
                if result:
                    self.clear()         ##Calling the clear method
                    print(f"Your IP Address is Up {user_ip_address}".center(shutil.get_terminal_size().columns))  
                    device_type = input("Enter your Device Type (cisco_ios,Juniper):- ").strip().lower()
                    user_name = input("Enter Username: ").strip()
                    user_pass = advpass() if os.name == "nt" else askpass()
                    if any(" " in x or len(x) == 0 for x in [user_name, user_pass, user_ip_address, device_type]):
                        Text_Style.common_text(
                            primary_text=Text_File.error_text["wrong_value"],
                            primary_text_style="bold",
                            primary_text_color="red"
                        )
                        counter_start += 1          ##Counter Increased
                    else:
                         return {
                            "device_type":device_type,
                            "host":user_ip_address,
                            "username":user_name,
                            "password":user_pass
                            }       
                else:
                    self._clear_screen()
                    print(f"Your IP Address is not up. Please check it again: {user_ip_address}".center(shutil.get_terminal_size().columns, "!"))
            print("!!! You have reached your limit !!!")
            return ("", "", "")
        except ValueError as value:
            print(f'Function: {__name__}, Exception: {type(value).__name__}')
        except Exception as e:
            print(f'Function: {__name__}, Exception: {type(e).__name__}')


    def _multiple_device_auth_data(self) -> list:
        user_input = int(input(Text_Style.common_text(primary_text=Text_File.common_text["user_choice_no"],add_line_break=False)))
        counter = 0
        max_counter = 3
        device_details_list = []
        try:
            while counter < max_counter:
                for i in range(user_input):
                    device_ip = input(Text_Style.common_text(primary_text=Text_File.common_text["ip_address_range"],add_line_break=False)).strip()
                    device_type = input(Text_Style.common_text(primary_text=Text_File.common_text["device_type"],add_line_break=False)).strip().lower()
                    user_name = input(Text_Style.common_text(primary_text=Text_File.common_text["username"],add_line_break=False)).strip()
                    user_pass = advpass() if os.name == "nt" else askpass(prompt=Text_File.common_text["password"])
                    
                    if any(" " in x or len(x) == 0 for x in [user_name, user_pass, device_ip, device_type]):
                        Text_Style.common_text(
                            primary_text=Text_File.error_text["wrong_value"],
                            primary_text_style="bold",
                            primary_text_color="red"
                        )
                        counter += 1
                    else:
                        device_details_list.append({
                            "device_type": device_type,
                            "host": device_ip,
                            "username": user_name,
                            "password": user_pass
                        })
                return device_details_list
            Text_Style.common_text(
                primary_text=Text_File.error_text["limit_exceed"],
                primary_text_style="bold",
                primary_text_color="red"
            )
        except Exception as e:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["common_function_exception"],
                primary_text_style="bold",
                secondary_text=e,
                secondary_text_color="red",
                secondary_text_style="bold"
            )

