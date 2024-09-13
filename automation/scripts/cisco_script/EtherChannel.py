
from assets.text_file import Text_File
import automation.components.etherchannel_functions as modules
import sys

handlerfunction_items = {"1":modules.etherchannel_functions.show_etherchannel_details,"2":modules.etherchannel_functions.configure_etherchannel,"3":modules.etherchannel_functions.exitmenu}


etherchannel_menu_items = ["Show EtherChannel","Configure EtherChannel","Exit"]

##EtherChannel Function
def Etherchannel(netmiko_connection)->None:
    try:
        print("Here we will call the menu rendered function")
        modules.etherchannel_functions.menu_renderer(data=etherchannel_menu_items)  ##need to change
        handler_key = input(Text_File.common_text["user_choice_no"])
        result = modules.etherchannel_functions.handlerfunction(key=handler_key,handler_functions_list=handlerfunction_items,connection = netmiko_connection)
        if result:
            return result       ##If result is True
        else:
            sys.exit()          ##If result is False

    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

##Main Function
def main(connection:object)->None:
    return Etherchannel(connection)

##Calling the Main Function
if __name__ == "__main__":
    result = main()
