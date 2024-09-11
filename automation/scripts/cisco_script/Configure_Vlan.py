from assets.text_file import Text_File
from tabulate import tabulate
from automation.scripts.cisco_script.Configure_Interface import configuration_menu


menu_item = ["Vlan Configuration","Exit"]       ##Menu items List
def Configure_Vlan(*args, **kwargs):
    netmiko_connection = args[0]            ##Getting the args
    try:
        vlan_info = netmiko_connection.send_command("show ip interface brief",use_textfsm=True)
        configuration_menu(menu_item)           ##Rendered the items
        case_key = input(Text_File.common_text["User_choice"])

    except Exception as e:
        print(f"This is the exception of the function",e)
   


##Main Function
def main(*args, **kwargs):
    return Configure_Vlan(*args, **kwargs)

##Calling the Main Function
if __name__ == "__main__":
    main()

