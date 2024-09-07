from typing import List,Dict
from netmiko import ConnectHandler
import shutil
from assets.text_file import Text_File

class Device_Connection:
    def __init__(self,HOST_IP_ADDRESS,USERNAME,PASSWORD,PORTNO=22) -> None:
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
                "username":self.USERNAME,
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

    #Multiple Method for Connecting to the device
    def multipl_device_connection(self)->object:
        try:
            for HOSTIP in self.HOSTIPADDDRESS:
                result = self.__device_details(HOSTIP,self.USERNAME,self.PASSWORD)
                if type(result) == dict:
                    print(f"{Text_File.debug_text["device_details"]}".center(shutil.get_terminal_size().columns),"*")
                    print(f"{Text_File.common_text["connected_host"]}{result["host"]}".center(shutil.get_terminal_size().columns,"*"))
                    netmiko_connection = ConnectHandler(**result)
                    return netmiko_connection
                else:
                    print(Text_File.error_text["device_details_error"])
                    return None
        
        except ValueError as value:
            print(Text_File.exception_text["value_error"],value)
            return None
        
        except Exception as e:
            print(Text_File.exception_text["common_function_exception"],e)
            return None

