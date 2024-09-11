from assets.text_file import Text_File
from tabulate import tabulate
from automation.scripts.cisco_script.Configure_Interface import configuration_menu,dynamic_match

##Show vlan_details
def show_vlan_details(*args)->str:
    vlan_details = args[2]
    try:    
        header = ["Vlan Id","Vlan Name","Status"]
        table_data = []
        for data in vlan_details:
            row = [data.get("vlan_id"),
                   data.get("vlan_name"),
                   data.get("status")]
                   
            table_data.append(row)
        table_string = (tabulate(table_data, header, tablefmt="heavy_grid"))
        print(table_string)
        return table_string
        
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"])

##list items of the menu
def vlan_configuration_menu()->None:
    vlan_configuration_menu = ["Create Vlan","Delete Vlan","Exit"]
    try:
        for sequence,vlan_menu in enumerate(vlan_configuration_menu,start=1):
            print(f"({sequence}) {vlan_menu}")
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"])

##Create Vlan Function
def create_vlan(*args)->None:
    try:
        netmiko_connection = args[2]
        user_vlan_starting_range = int(input(Text_File.common_text["vlan_starting_range"]))
        user_vlan_ending_range = int(input(Text_File.common_text["vlan_ending_range"]))
        for vlanno in range(user_vlan_starting_range,user_vlan_ending_range+1):
            output = netmiko_connection.send_config_set([f"vlan {vlanno}"])
            print(output)
        return(f"Your total vlan have been created {user_vlan_ending_range-user_vlan_starting_range}")

    except ValueError as value:
        print(Text_File.exception_text["value_error"],value)
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

##Delete Vlan Function
def delete_vlan(*args)->None:
    try:
        netmiko_connection = args[2]
        user_vlan_starting_range = int(input(Text_File.common_text["vlan_starting_range"]))
        user_vlan_ending_range = int(input(Text_File.common_text["vlan_ending_range"]))
        for vlanno in range(user_vlan_starting_range,user_vlan_ending_range+1):
            output = netmiko_connection.send_config_set([f"no vlan {vlanno}"])
            print(output)
        return(f"Your total vlan have been deleted {user_vlan_ending_range-user_vlan_starting_range}")
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"])

##Configure the vlan
def configure_vlan(*args)->any:
    netmiko_connection = args[3]            ##netmiko object
    configure_handler_details = {"1":create_vlan,"2":delete_vlan}       ##Configure vlan handler details
    try:
        if show_vlan_details(*args):
            user_choice = input(Text_File.common_text["vlan_configuration_permission"]).strip().lower()
            if user_choice == "yes":
                vlan_configuration_menu()
                case_key1 = input(Text_File.common_text["User_choice"])
                result = dynamic_match(case_key1,configure_handler_details,netmiko_connection)
                return result
      
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)


handler_details ={"1":show_vlan_details,"2":configure_vlan}        ##Handlers
menu_item = ["Show Vlan","Configure Vlan"] ##Menu items List
      
def Configure_Vlan(netmiko_connection):          ##Getting the args
    try:
        vlan_info = netmiko_connection.send_command("show vlan",use_textfsm=True)
        configuration_menu(menu_item)           ##Rendered the items
        case_key = input(Text_File.common_text["User_choice"])
        result = dynamic_match(case_key,handler_details,vlan_info,netmiko_connection)
        return result       ##Returning the function output
    
    except Exception as e:
        print(f"This is the exception of the function",e)
   
##Main Function
def main(netmiko_connection):
    return Configure_Vlan(netmiko_connection)

##Calling the Main Function
if __name__ == "__main__":
    main()

