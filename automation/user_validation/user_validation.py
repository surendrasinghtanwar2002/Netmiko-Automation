from assets.text_file import Text_File

##Method to check the enable mode
def enable_mode(netmiko_connection:object)->list:
    try:
        if netmiko_connection.enable():
            print("Your Device is in Enable mode")
            return True
    except ValueError as value:
        print(Text_File.exception_text["value_error"],value)
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)
    
