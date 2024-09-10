from maskpass import askpass
from assets.text_file import Text_File
import shutil
import os
import platform

##clear screen function
def clear()->None:
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

##single_device_connection_auth
def single_device_auth():                                   
    try:
        clear()
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


##Multiple device connection
def multiple_device_auth()->tuple[str,str,list]:
    print(Text_File.common_text["mutli_auth_welcome"])
    try:
        clear()
        user_pass_confirm = input(Text_File.common_text["same_credentials"]).strip().lower() or "yes"
        print(f"-------> {user_pass_confirm} <------------ Degubiggin this code")
        if user_pass_confirm == "yes":
            starting_range = 1              ##Counter value for loop statement
            my_ip_address_list = []             ##IP ADDRESS LIST
            user_name = input(Text_File.common_text["username"])
            user_pass = askpass(Text_File.common_text["password"])            
            user_ip_choice = int(input((Text_File.common_text["range_of_ip"])))
            while starting_range < user_ip_choice+1:
                ip_address = input(f"{Text_File.common_text["ip_address_range"]} ({starting_range}):-")
                my_ip_address_list.append(ip_address)
                starting_range+=1           ##Counter value will increase here
                
            return user_name,user_pass,my_ip_address_list           ##Return the value after the completion
            
    except ValueError as value:
        print(f"{Text_File.exception_text["value_error"]} {value}")
        
    except Exception as e:
        print(f"{Text_File.exception_text["common_function_exception"]}",e)
    
    return None ##It will None if any exception will arise


def main()->None:
    multiple_device_auth()
    single_device_auth()


if __name__ == "__main__":
    main()


