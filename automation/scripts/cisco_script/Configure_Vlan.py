from assets.text_file import Text_File
from tabulate import tabulate
from automation.scripts.cisco_script.Configure_Interface import configuration_menu,dynamic_match
import re
import shutil

##Show vlan_details Menu
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
        print(Text_File.exception_text["common_function_exception"],e)

##list items of the menu
def vlan_configuration_menu()->None:
    vlan_configuration_menu = ["Create Vlan","Delete Vlan","Assigned Interface to Vlan","Configure Vlan IP Address"]
    try:
        for sequence,vlan_menu in enumerate(vlan_configuration_menu,start=1):
            print(f"({sequence}) {vlan_menu}")
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

##Create Vlan Function
def create_vlan(*args)->None:
    try:
        netmiko_connection = args[2]
        ##taking user choice for creating the vlan
        user_vlan_choice = int(input(Text_File.common_text["vlan_create_range"]))
        if user_vlan_choice == 1:
            user_vlan = int(input(Text_File.common_text["vlan_no_input"]))
            single_vlan = netmiko_connection.send_config_set(f"vlan {user_vlan}")
            return single_vlan
        ##taking multiple user choice
        else:
            user_vlan_starting_range = int(input(Text_File.common_text["vlan_starting_range"]))
            user_vlan_ending_range = int(input(Text_File.common_text["vlan_ending_range"]))
            for vlanno in range(user_vlan_starting_range,user_vlan_ending_range+1):
                vlan_no_command = [f"vlan {vlanno}"]            ##passing a command for the execution
                output = netmiko_connection.send_config_set(vlan_no_command)
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
            vlan_no_command = [f"no vlan {vlanno}"]
            output = netmiko_connection.send_config_set(vlan_no_command)
            print(output)
        return(f"Your total vlan have been deleted {user_vlan_ending_range-user_vlan_starting_range}")
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

##Interface Details Function
def interface_details_print(netmiko_connection):
    try:
        table_data = []
        header = ["Interface Name","Ip Address","Status","Prototype"]
        output = netmiko_connection.send_command("show ip interface brief",use_textfsm=True)            ##Return the dictionary
        for data in output:
            row = [data.get("interface"),
                   data.get("ip_address"),
                   data.get("status"),
                   data.get("proto")
                   ]
            table_data.append(row)
         ##display the items
        print(tabulate(table_data, header, tablefmt="heavy_grid"))

    except Exception as e:
        print(Text_File.exception_text["common_function_exception"])

##Allocate Interface to the vlan
def allocate_interface(*args)->str:
    try:
        netmiko_connection = args[2]
        interface_details_print(netmiko_connection)             ##This will print the interface details
        print(Text_File.common_text["Interface_Details"])
        vlan_interface_starting = input(Text_File.common_text["vlan_interface_starting"])
        vlan_interface = int(input(Text_File.common_text["vlan_interface"]))
        interfaces = []         ##interfaces name
        range_pattern = re.match(r"([a-zA-Z]*[a-zA-Z]*)[\d/]+/(\d+-\d+)", vlan_interface_starting)  ##Pattern Matching GigabitEthernet1/0/1-5
        if range_pattern:
            # basename = vlan_interface_starting.split("/") [0]               ##it will split the base Interface Name with
            start, end = map(int, range_pattern.group(2).split('-'))
            prefix = vlan_interface_starting.rsplit('/', 1)[0]
            for i in range(start, end + 1):
                interfaces.append(f"{prefix}/{i}")

        # Handling specific interfaces like GigabitEthernet1/0/1, GigabitEthernet1/0/3
        elif ',' in vlan_interface_starting:
            interfaces = [iface.strip() for iface in vlan_interface_starting.split(',')]
        # Handling single interface input
        else:
            interfaces.append(vlan_interface_starting.strip())

        all_output = ""
        for interface in interfaces:
            commands = [f"interface {interface}",f"switchport access vlan {vlan_interface}","no shutdown"]
            output = netmiko_connection.send_config_set(commands)        ##sending netmiko commands to the device
            print(output)                                                ##used for debugging purpose
            all_output+= output
        return f"Your All Commands Output".center(shutil.get_terminal_size().columns,"!") +"\n" +all_output
        
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],__name__,e)

##Allocate Ip to the vlan interface
def configure_vlan_ip(*args)->str:                              ##Still not working 
    try:
        netmiko_connection = args[2]
        show_vlan_details(*args)
        print(Text_File.common_text["Interface_Details"])
        vlan_no = int(input("Please Enter your Vlan Number from the above list (eg. 10,20,30):- "))
        ip_address = input("Please Enter your Ip Address eg:(192.168.1.1):- ").strip()
        subnet_mask = input("Please Enter your Subnet Mask:-").strip()
        commands = [f"vlan {vlan_no}",f"ip address {ip_address+ " " +subnet_mask}","no shut"]
        output = netmiko_connection.send_config_set(commands)
        print(output)
        return output

    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

##Vlan Configuration Menu
def configure_vlan_menu(*args)->any:
    netmiko_connection = args[3]                                        ##netmiko object
    configure_handler_details = {"1":create_vlan,"2":delete_vlan,"3":allocate_interface,"4":configure_vlan_ip}       ##Configure vlan handler details
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


handler_details ={"1":show_vlan_details,"2":configure_vlan_menu}        ##Main Menu Handlers
menu_item = ["Show Vlan","Configure Vlan","Exit"]                       ##Main Menu Items list



##main Menu Function
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

