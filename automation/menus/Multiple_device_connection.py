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
    def __init__(self, list) -> None:
        self.device_details = list
        self.netmiko_devices_connection = []  # A list to store the netmiko device connections

    def netmiko_connection(self, device) -> object:
        try:
            with ConnectHandler(**device) as connection:
                print(f"Connected to {device['host']}")
                return connection
        except Exception as e:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["connection_failed"],
                secondary_text=device['host'], 
                secondary_text_color="red"
            )


    def threading_module(self) -> bool:
        try:
            with ThreadPoolExecutor(max_workers=5) as executor:
                self.netmiko_devices_connection = list(executor.map(self.netmiko_connection, self.device_details))
                Global_State_Manager.Netmiko_State_Push_Manager(device=self.netmiko_devices_connection)  # Add connections to global state manager
                return True
        except Exception as e:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["common_function_exception"],
                secondary_text=str(e),
                secondary_text_color="red"
            )

    # Method for filtering devices from the list
    @staticmethod
    def __filter_method(device) -> bool:
        return "host" in device

    def _ip_address_validation(ip_address: list) -> list:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        valid_ip_addresses = []  # valid IP addresses list
        try:
            if isinstance(ip_address, list):
                print("Multiple IP Address Pinging Method")  # Debug purpose
                for ip in ip_address:
                    host = ip
                    command = ["ping", param, "2", host]
                    if subprocess.call(command) == 0:
                        valid_ip_addresses.append(ip)  # Append valid IP addresses
                    else:
                        Text_Style.common_text(
                            primary_text=f"{Text_File.error_text['Unvalid_ip_address']} {ip}",
                            primary_text_style="bold",
                            primary_text_color="red"
                        )
                return valid_ip_addresses
        except subprocess.CalledProcessError as processerror:
            Text_Style.common_text(
                primary_text=f"Function: {__name__}",
                primary_text_style="bold",
                secondary_text=f"{type(processerror).__name__}",
                secondary_text_color="red",
                secondary_text_style="bold"
            )

    @staticmethod
    def __printing_valid_ip_address_table(host_ip: list) -> None:
        table_data = []
        header = ["Sequence", "Ip_Address"]
        for sequence, ip_address in enumerate(host_ip, start=1):
            table_data.append([sequence, ip_address])
        print(tabulate(table_data, header, tablefmt="double_outline").center(shutil.get_terminal_size().columns))

    def multiple_host_connection(self) -> None:
        try:
            result = Text_Style.progress_bar()
            if result:
                device_details = self.__multiple_device_auth_data()
                filtered_devices = filter(self.__filter_method, device_details)  # Use filter to get devices with the 'host' key
                ip_addresses = [device["host"] for device in filtered_devices]  # Extracting IP addresses
                valid_ip_address = self.__ip_address_validation(ip_address=ip_addresses)
                user_choice = input(Text_Style.common_text(primary_text=Text_File.common_text["print_ip_table"])).strip()
                if user_choice == "yes":
                    self.__printing_valid_ip_address_table(host_ip=valid_ip_address)
                else:
                    pass
        except Exception as e:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["common_function_exception"],
                secondary_text=str(e),
                secondary_text_color="red"
            )





