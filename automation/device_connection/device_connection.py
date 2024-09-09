from typing import Tuple, Union,Dict,List
from netmiko import ConnectHandler
import shutil
import subprocess
import platform
from assets.text_file import Text_File
from tabulate import tabulate
from automation.authentication.authentication import clear

class Device_Connection:
    def __init__(self,USERNAME,PASSWORD,HOST_IP_ADDRESS,PORTNO=22) -> None:
        self.HOSTIPADDDRESS = HOST_IP_ADDRESS
        self. USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.PORTNO = PORTNO
    
    #First Method for Connecting to the device
    def single_device_connection(self)->object:
        try:
            device_details = {
                "device_type":"cisco_ios",
                "host":self.HOSTIPADDDRESS,
                "username":self. USERNAME,
                "password":self.PASSWORD,
                "port":self.PORTNO
            }
            netmiko_connection = ConnectHandler(**device_details)
            print(f" {Text_File.common_text["connection"]} {device_details["host"]} ".center(shutil.get_terminal_size().columns),"*")
            return netmiko_connection

        except ValueError as value:
            print(f"{Text_File.exception_text["value_error"]}",value)
            return None
                
        except Exception as e:
             print(f"{Text_File.exception_text["common_function_exception"]}",e)
             return None
    
    
    ##device details generator
    def __device_details(self,HOSTIP,username,password)->Dict:
        try:
            return{"device_type":"cisco_ios","host":HOSTIP,"username":username,"password":password,"port":self.PORTNO}
        
        except ValueError as value:
            print(f"{Text_File.exception_text["value_error"]}",value)
        
        except Exception as e:
            print(f"{Text_File.exception_text["common_function_exception"]}",e)


    ##pinging the machine
    @staticmethod
    def __pinging_machine(host: List[str], timeout: int = 4) -> Tuple[List[str], List[str]]:
        valid_ip_address = []

        for ip_address in host:
            try:
                if platform.system().lower() == 'windows':
                    cmd = ['ping', ip_address, '-n', '1', '-w', str(timeout * 1000)]
                else:
                    cmd = ['ping', ip_address, '-c', '1', '-W', str(timeout)]

                result = subprocess.run(cmd, capture_output=True, text=True, check=False)

                if result.returncode == 0:
                    valid_ip_address.append(ip_address)
                else:
                    pass

            except subprocess.CalledProcessError as e:
                print(f"{Text_File.error_text["CalledProcessError a"]} {e}")

        return valid_ip_address

    ##priting the table
    @staticmethod
    def __printing_valid_ip_address_table(host_ip:List[str])->None:         ##Method to print the valid ip address
        clear()         ##Clear Screen Function
        table_data = []
        header = ["Sequence","Ip_Address"]
        for sequence,ip_address in enumerate(host_ip,start=1):
            table_data.append([sequence,ip_address])
        print(tabulate(table_data,header,tablefmt="double_outline").center(shutil.get_terminal_size().columns))
    
    #Multiple Method for Connecting to the device
    def multipl_device_connection(self)->object:
        try:
            validip = self.__pinging_machine(self.HOSTIPADDDRESS) ##This function will filter the server which are responding
            self.__printing_valid_ip_address_table(validip)
            user_choice = input(f"{Text_File.common_text["proceed_confirmation"]}").strip().lower()
            if user_choice == "yes":
                for HOSTIP in validip:                  
                    print(f"{Text_File.debug_text["device_respond"]} {HOSTIP}")
                    result = self.__device_details(HOSTIP,self.USERNAME,self.PASSWORD)
                    if isinstance(result,dict):
                        print(f"{Text_File.debug_text["device_details"]}".center(shutil.get_terminal_size().columns),"*")
                        print(f"{Text_File.common_text["connected_host"]}{result["host"]}".center(shutil.get_terminal_size().columns,"*"))
                        netmiko_connection = ConnectHandler(**result)
                        return netmiko_connection
                    else:
                        print(Text_File.error_text["device_details_error"])
                        return None
            else:
                print("Quiting the code")           ##Need to change
        
        except ValueError as value:
            print(Text_File.exception_text["value_error"],value)
            return None
        
        except Exception as e:
            print(Text_File.exception_text["common_function_exception"],e)
            return None

