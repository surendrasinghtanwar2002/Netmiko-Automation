import typing
from assets.text_file import Text_File
##Get Running-Config Details
def get_running_config(*args:typing.Tuple[typing.Any],**kwargs:typing.Dict[str, typing.Any])-> typing.Optional["str"]:
    try:
        netmiko_connection = args           ##unwrapping the tupple
        result = netmiko_connection.send_command ("show running-config",strip_prompt = False, strip_command = False)
        if result:
            print(Text_File.common_text["Data_retrieved"])
            return result
        else:
            print(Text_File.error_text)
            return result

    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)


##Main function calls here 
def main()->None:
    get_running_config()


##calling the main function
if __name__ == "__main__":
    main()



    
