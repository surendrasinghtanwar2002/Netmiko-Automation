from assets.text_file import Text_File
import sys
from tabulate import tabulate
from time import sleep
import re
import shutil
         
         
         ##EtherChannel Menu Items
etherchannel_menu_items = ["Show EtherChannel","Configure EtherChannel","Exit"]

lacp_configuration_menu_items = ["LACP Fast Mode","LACP System Priority","LACP Interface Priority","Port Channel Member Interfaces Maximum Number","Port Channel Member Interfaces Minimum Number"]
           ## This function is used to render the Menu Items
def menu_renderer(data:list|str)->None:
    try:
        for sequenceno,items in enumerate(data,start=1):
            print(f"({sequenceno}) {items}")
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

                    ## This function is used to handle menu all configuration functions
def handlerfunction(key:str,handler_functions_list:dict,connection:object):
    try:
        handler_connection = handler_functions_list.get(key,exitmenu)       ##In this section if key is not able to find then exit menu will run
        result = handler_connection(connection)
        return result               ##This function is returning the handler function output
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)


                    ## This function will convert data in table format
def tablulaconvertor(data):
    try:
        table_header = ["GroupNo","Port Channel","Protocol","Ports","Status"]
        for items in data:
            row = [items.get["group"],
                   items.get["port_channel"],
                   items.get["protocol"],
                   items.get["ports"],
                   items.get["status"]
                   ]
        print(tabulate(row,table_header,tablefmt="grid"))
        print(f"Let;s check either we have received the data or not {data}")
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

                    ## This all functions are etherchannel configuration Functions##
def show_etherchannel_details(netmiko_connection):
    try:
        etherchannel_result = netmiko_connection.send_command("show etherchannel summary",use_textfsm=True)
        tablulaconvertor(data=etherchannel_result)      ##This function is used to print data in tabulate format or table format
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)
        return False

def exitmenu():
    try:
        sys.exit()          ##This method will close the python script
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)
        return False

                    ## Configuration EtherChannel menu and all their function will be here ##

##Interface details print
def interface_details(netmiko_connection: object)->None:
    try:
       result = netmiko_connection.send_command("show ip interface brief",use_textfsm=True)
       table_data = []          ##This is the list where data items will get stored
       for items in result:
           row = [items.get["interface"],
                  items.get["ip_address"],
                  items.get["status"],
                  items.get["proto"]
                  ]
           table_data.append(row)

       print(tabulate(table_data,headers=["Interface Name","Ip Address","Status","Prototype"],tablefmt="grid"))
           
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

##interface configuration function
def interface_validation()->list["str"]:
    try:
        user_interfaces = input("Enter your interface_range from the above list:- ")
        interfaces = []             ##interfaces_details
        pattern = r"([a-zA-Z]*[a-zA-Z]*)[\d/]+/(\d+-\d)"
        range_pattern = re.match(pattern,user_interfaces)
        if range_pattern:                                           ##Used to handle details like GigabitEthernet1/0/1-GigabitEthernet1/0/3 (Interface range)
            start, end = map(int, range_pattern.group(2).split('-'))
            prefix_value = user_interfaces.rsplit("/",1)[0]         ##In this section we have split the prefix value from the range
            for i in range(start,end+1):
                interfaces.append(f"{prefix_value}/{i}")
        elif "," in user_interfaces:                               ##It is used to split the interface such as GigabitEthernet1/0/1,-GigabitEthernet1/0/3
            interfaces = [iface.strip() for iface in user_interfaces.split(',')]
        else:
            interfaces.append(user_interfaces.strip())          ##Single interface handle 
        print("We will print the interface configuration details")
    except Exception as e:
        print(f"This is the exception",e)

def channel_group_configuration(netmiko_connection,interfaces_items,user_mode_selection):
    try:
        print(f"Yes we have received the netmiko object {netmiko_connection}")
        user_group_no = int(input("Enter your group number (eg:- 1,10,20,30):-").strip())

        commands = [f"interface {interfaces_items}",f"channel-group {user_group_no} mode {user_mode_selection}"]
        result = netmiko_connection.send_config_set(commands)
        return result
    except Exception as e:
        print(f"Yes we have an exception in our function",e)

##Pagp Configuration
def pagp_connection(connection: object)->None:
    try:
        user_input = input("Do you want to print the Interface Details (Yes/No):- ").strip().lower()
        if user_input == "yes":
            interface_details()
            interfaces = interface_validation()             ##Interface validation have return the interfaces
            print(f"-----------> {interfaces} <----------")
            user_mode = input("Enter your configuration mode: (Auto/Desirable)").strip().lower()
            result = channel_group_configuration(netmiko_connection=connection,interfaces_items=interfaces,user_mode_selection=user_mode)
            return result
        else:
            interfaces = interface_validation()
            print(f"-----------> {interfaces} <----------")
            result = channel_group_configuration(netmiko_connection=connection,interfaces_items=interfaces)
            return result
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)


                                                        ## Lacp Configuration All Function ##
##Function used to configure the fast mode and slow mode
def lacp_Fast_Mode_configuration():
    try:
        print("In this section we will perform the lacp fast mode configuration")

    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

##Function use to set the system priority to choose the portchannel master switch
def lacp_System_Priority(netmiko_connection):
    try:
        print("In this section we will perform the lacp system priority configuration")
        result = netmiko_connection.send_command("show lacp sys-id")
        print(f"This is your system priority value \n {result}")
        user_choice = input("Do you wan;t to make changes in priority (Yes/No):- ").strip().lower()
        if user_choice == "yes":
            user_system_priority = int(input("Enter your system priority (eg: 1,3,5,7):-".strip()))
            result = netmiko_connection.send_command(f"lacp system-priority {user_system_priority}")
            return result               ##simply return the system command output
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

##Function use to set the interface priority 
def lacp_interface_priority(netmiko_connection):
    try:
        print(f"-------------->{netmiko_connection} <-------------")
        print("We are working on that we will inform you whenever this functionalities get completed")
            
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"])

##Function use to set Port Channel Member Interfaces Maximum Number
def port_channel_max_interface(netmiko_connection):
    try:
        print(f"Netmiko Connection object status {netmiko_connection}")         ###used for debugging purpose only
        print("Wait we are loding the interface details choose your interface and apply the configuration.....")
        sleep(2)                ##sleeper for 2 seconds
        interface_details(netmiko_connection)
        user_interface_name = input("Enter your interface name from the above list:- ").strip()
        user_interface_value = int(input("Enter your max number to be allocated to port channel:- ").strip())
        if user_interface_name and user_interface_value:
            print("You'r Details are valid please wait we are confirming with the device")
            sleep(2)            ##Sleeper for 2 second
            commands = [f"interface {user_interface_name}",f"lacp max-bundle {user_interface_value}"]
            result = netmiko_connection.send_config_set(commands)
            return result           ##simply returning the result

    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

##Function use to set Port Channel Member Interface Minimum Number
def port_channel_min_interface(netmiko_connection):
    try:
        print(f" Netmiko connection object status {netmiko_connection} ".center(120,"*"))
        print("Wait we are loding the interface details choose your interface and apply the configuration.....")
        sleep(2)                ##sleeper for 2 seconds
        interface_details(netmiko_connection)
        user_interface_name = input("Enter your interface name from the above list:- ").strip()
        user_interface_value = int(input("Enter your max number to be allocated to port channel:- ").strip())
        if user_interface_name and user_interface_value:
            print("Your details are valid please wait we are confirming with the device")
            sleep(2)                ##sleeper for 2 seconds
            commands = [f"interface {user_interface_name}",f"lacp max-bundle {user_interface_value}"]
            result = netmiko_connection.send_config_set(commands)
            return result           ##simply returning the result
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)


##lacp handler function mapper list
lacp_handler_items = {"1":lacp_Fast_Mode_configuration,"2":lacp_System_Priority,"3":lacp_interface_priority,"4":port_channel_max_interface,"5":port_channel_min_interface}


##Lacp Configuration
def lacp_configuration(connection: object)->None:
    try:
        user_input = input("Do you want to print the Interface Details:- ").strip().lower()
        if user_input == "yes":
            interface_details()
            interfaces = interface_validation()
            print(f"-----------> {interfaces} <----------")
            user_mode = input("Enter your configuration mode: (Active/Passive)").strip().lower()
            result = channel_group_configuration(netmiko_connection=connection,interfaces_items=interfaces,user_mode_selection=user_mode)
            print(" Your configuration have been configured succesfully ".center(shutil.get_terminal_size().columns,"!"))
            print(f"\n{result}")
            next_menu_permission = input("Do you want to configure Additional Properties of Lacp:- ").strip().lower()
            if next_menu_permission == "yes":
                menu_renderer(data=etherchannel_menu_items)
                user_key = input("Enter your choice from the above list:- ").strip().lower()
                handlerfunction(key=user_key,handler_functions_list=lacp_handler_items,connection=connection)
        else:
            result = interface_validation()
            print(result)

    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

##handler_functions list
handler_list = {"1":pagp_connection,"2":lacp_configuration,"3":exitmenu}

def configure_etherchannel(netmiko_connection):
    try:
        user_choice = input("Do you want to continue (Yes/No):- ").strip().lower()
        if user_choice == "yes":
            menu_renderer(data=lacp_configuration_menu_items)
            handler_key = input(Text_File.common_text["user_choice_no"])
            result = handlerfunction(key=handler_key,handler_functions_list=handler_list,connection=netmiko_connection)
            return result
        else:
            return False

    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)
        return False

