
from assets.text_file import Text_File
import components.all_menu_items_list as menuitems
import components.etherchannel_functions as etherchannelfunction
import sys

handlerfunction_items = {"1":etherchannelfunction.show_etherchannel_details,"2":etherchannelfunction.configure_etherchannel,"3":etherchannelfunction.exitmenu}

##EtherChannel Function
def Etherchannel(netmiko_connection)->None:
    try:
        print("Here we will call the menu rendered function")
        etherchannelfunction.menu_renderer(data=menuitems.etherchannel_menu_items)
        handler_key = input(Text_File.common_text["user_choice_no"])
        result = etherchannelfunction.handlerfunction(key=handler_key,handler_functions_list=handlerfunction_items,connection = netmiko_connection)
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
