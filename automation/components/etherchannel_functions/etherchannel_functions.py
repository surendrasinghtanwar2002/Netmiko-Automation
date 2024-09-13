from assets.text_file import Text_File
import sys
from tabulate import tabulate
import all_menu_items_list
from time import sleep
import re
                    ## This function is used to render the Menu Items
def menu_renderer(data:list|str)->None:
    try:
        for sequenceno,items in enumerate(data,start=1):
            print(f"({sequenceno}) {items}")
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

                    ## This function is used to handle menu all configuration functions
def handlerfunction(key,handler_functions_list,connection):
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


##interface configuration
def interface_configuration():
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

##Pagp Configuration
def pagp_connection(netmiko_connection: object)->None:
    try:
        user_input = input("Do you want to print the Interface Details:- ").strip().lower()
        if user_input == "yes":
            interface_details()
            result = interface_configuration()
            print(result)
        else:
            result = interface_configuration()
            print(result)

    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

##Lacp Configuration
def lacp_configuration(netmiko_connection: object)->None:
    try:
        user_input = input("Do you want to print the Interface Details:- ").strip().lower()
        if user_input == "yes":
            interface_details()
            result = interface_configuration()
            print(result)
        else:
            result = interface_configuration()
            print(result)

    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

##handler_functions list
handler_list = {"1":pagp_connection,"2":lacp_configuration,"3":exitmenu}

def configure_etherchannel(netmiko_connection):
    try:
        user_choice = input("Do you want to continue (Yes/No):- ").strip().lower()
        if user_choice == "yes":
            menu_renderer(data=all_menu_items_list)
            handler_key = input(Text_File.common_text["user_choice_no"])
            result = handlerfunction(key=handler_key,handler_functions_list=handler_list,connection=netmiko_connection)
            return result
        else:
            return False

    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)
        return False

