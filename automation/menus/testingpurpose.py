from concurrent.futures import ThreadPoolExecutor
from state.global_State_Manger import Global_State_Manager
from assets.text_style import Text_Style
from assets.text_file import Text_File
from netmiko import ConnectHandler
from tabulate import tabulate
from maskpass import advpass, askpass
import shutil
import platform
import subprocess
import os

class MultipleDeviceConnection:
    def __init__(self, device_details: list) -> None:
        self.device_details = device_details,
        self.netmiko_devices_connection = []                ## A list to store the netmiko device_connection

    def netmiko_connection(self, device)->object:
        try:
            with ConnectHandler(**device) as connection:
                print(f"Connected to {device['host']}")
                return connection
        except Exception as e:
            Text_Style.common_text(primary_text=Text_File.exception_text["connection_failed"],secondary_text=device['host'],secondary_text_color="red")

    def threading_module(self)->bool:
        try:
            with ThreadPoolExecutor(max_workers=5) as executor:
                self.netmiko_devices_connection=list(executor.map(self.netmiko_connection, self.device_details))
                Global_State_Manager.Netmiko_State_Push_Manager(device=self.netmiko_devices_connection)         ##Adding the netmiko device connection to the global state manager
                return True
        except Exception as e:
            Text_Style.common_text(primary_text=Text_File.exception_text["common_function_exception"],secondary_text=e,secondary_text_color="red")

    def __multiple_device_auth_data(self)->None:
        user_input = input(Text_Style.common_text(primary_text=Text_Style.common_text["user_choice_no"]))
        counter = 0
        max_counter = 3
        device_Details_list = []
        try:
            while counter < max_counter:
                for i in range(user_input+1):
                    device_ip = input(Text_Style.common_text(primary_text=Text_Style.common_text["ip_address_range"])).strip()
                    device_type = input(Text_Style.common_text(primary_text=Text_Style.common_text["device_type"])).strip().lower()
                    user_name = input(Text_Style.common_text(primary_text=Text_Style.common_text["username"])).strip()
                    user_pass = advpass() if os.name == "nt" else askpass(prompt=Text_File.common_text["password"])
                    if " " in user_name and user_pass and device_ip and device_type or len(user_name) == 0 and len(user_pass) == 0 and len(device_ip) == 0 and len(device_type) == 0:
                        Text_Style.common_text(primary_text=Text_File.error_text["wrong_value"],primary_text_style="bold",primary_text_color="red")
                        counter +=1
                    else:
                        device_Details_list.append({"device_type":device_type,"host":device_ip,"username":user_name,"password":user_pass})
                return device_Details_list
            Text_Style.common_text(primary_text=Text_File.error_text["limit_exceed"],primary_text_style="bold",primary_text_color="red")
        except Exception as e:
            Text_Style.common_text(primary_text=Text_File.exception_text["common_function_exception"],primary_text_style="bold",secondary_text=e,secondary_text_color="red",secondary_text_style="bold")

    ##Method for filtering the device from the devices list
    def __filter_method(device:None):
         return "host" in device
    
    @staticmethod                   
    def __ip_address_validation(ip_address:list):  
        param = '-n' if platform.system().lower() == 'win32' else '-c'
        valid_ip_addresses = []  ## valid IP address list 
        try:
            if isinstance(ip_address, list):
                print("Multiple IP Address Pinging Method")  ## Debug purpose
                for ip in ip_address:
                    host = ip
                    command = ["ping", param, "2", host]
                    if subprocess.call(command) == 0:
                        valid_ip_addresses.append(ip)  ## Append valid IP addresses
                    else:
                        Text_Style.common_text(primary_text=f"{Text_File.error_text["Unvalid_ip_address"]} {ip}",primary_text_style="bold",primary_text_color="red")
                return valid_ip_addresses
        except subprocess.CalledProcessError as processerror:
            Text_Style.common_text(primary_text=f"Function: {__name__}",primary_text_style="bold",secondary_text=f"{type(processerror).__name__}",secondary_text_color="red",secondary_text_style="bold")

    @staticmethod
    def __printing_valid_ip_address_table(host_ip:list[str])->None:         ##Method to print the valid ip address
        # clear()         ##Clear Screen FunctionUnvalid_ip_address
        table_data = []
        header = ["Sequence","Ip_Address"]
        for sequence,ip_address in enumerate(host_ip,start=1):
            table_data.append([sequence,ip_address])
        print(tabulate(table_data,header,tablefmt="double_outline").center(shutil.get_terminal_size().columns))

    def Multiple_device_connection(self)->None:
        try:
            result = Text_Style.progress_bar()
            if result:
                device_details = self.__multiple_device_auth_data()
                filtered_devices = filter(self.__filter_method(), device_details)#Use filter() to get only those devices that have the key 'ip_address'
                ip_addresses = [(device["host"], device) for device in filtered_devices] # Extracting IP addresses and their values
                valid_ip_address = self.__ip_address_validation(ip_address=ip_addresses)
                user_choice = input(Text_Style.common_text(primary_text=Text_File.common_text["print_ip_table"])).strip()
                if user_choice == "yes":
                    self.__printing_valid_ip_address_table(host_ip=valid_ip_address)

                



        except Exception as e:
            Text_Style.common_text(primary_text=Text_File.exception_text["common_function_exception"],secondary_text=e,secondary_text_color="red")


