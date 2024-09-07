from maskpass import askpass
from assets.text_file import Text_File
import shutil

##single_device_connection_auth
def single_device_auth():
    try:
        counter_start = 0
        counter_end= 3
        while counter_start < counter_end:
            user_name = input(Text_File.common_text["username"])
            user_pass = askpass(Text_File.common_text["password"])
            HOST_IP_Address = input(Text_File.common_text["host_ip_prompt"])

            if user_name and user_pass and HOST_IP_Address:
                print(f"{Text_File.common_text["valid_cred"]}".center(shutil.get_terminal_size().columns))
                return user_name,user_pass,HOST_IP_Address
            
            else:
                counter_start +=1
                print(Text_File.exception_text["device_details_error"])

        print(f"{Text_File.error_text["limit_exceed"]}")
        return None
    
    except ValueError as value:
        print(f"{Text_File.exception_text["value_error"]} {value}")
        return None
    
    except Exception as e:
        print(f"{Text_File.exception_text["common_function_exception"]} {e}")
        return None


