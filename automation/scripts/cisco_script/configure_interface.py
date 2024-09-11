from assets.text_file import Text_File
import json
from tabulate import tabulate

##Configuration Menu Loop
def configuration_menu(menu_items:list)->None:
    try:
        for item_no,item_value in enumerate(menu_items,start=1):
            print(f"({item_no}) {item_value}")
    except ValueError as value:
        print(Text_File.exception_text["value_error"],value)
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],__name__,e)

##Get Interface Details
def interface_details(interface_details):
    try:
        user_input = input("Do you want interface details (Yes/No):- ").strip().lower()
        if user_input == "yes":
            print(f"This is your interface details:- \n {interface_details}")
            return interface_details
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)
        return False

##Convert python object into json string
def json_string_convert(interface_Details_Data):
    try:
        print("In this section we will convert python object into json string")
        result = json.dumps(interface_Details_Data)
        return result
    except ValueError as value:
        print("Value was not assigned",value)
    except Exception as e:
        print("Exception as except",e)

##Configuration Interface
def interface_validation(interface_detail,interface_name,new_ip = None ):
    try:
        interface_confirmation = next((items for items in interface_detail if items["interface"] == interface_name),None)
        if interface_confirmation:
            return [f"interface {interface_name}",f"ip address {new_ip}","no shut"]
        else:
            return None
    except ValueError as value:
        print(f"This is your value error {value}")

##Get Interface Details
def interface_configuration(interface_details,netmiko_connection):
    try:
        header = ["Interface Name","Ip Address","Status","Prototype"]
        table_data = []
        for data in interface_details:
            row = [data.get("interface"),
                   data.get("ip_address"),
                   data.get("status"),
                   data.get("proto")
                   ]
            table_data.append(row)
        ##display the items
        print(tabulate(table_data, header, tablefmt="heavy_grid"))
              
        user_input = input("Do you want to configure anything:-").strip().lower()
        if user_input == "yes":
            interface_name = input("Please Enter your Interface Name from the above list:- ")
            ip_address = input("Please Enter your Ip Address eg:(192.168.1.1):- ").strip()
            subnet_mask = input("Please Enter your Subnet Mask:-").strip()
            command = interface_validation(interface_detail=interface_details,interface_name=interface_name,new_ip= (ip_address+" "+subnet_mask))
            if command:
                output = netmiko_connection.send_config_set(command)
                print(output)
        else:
            print("We are not able to process on the work")
            
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)
        return False

##Default Execution
def default_execution():
    try:
        print("Handle the Default statement")
        return False
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

##dynamic Match Function
def dynamic_match(case_key,*args):
    handler = {
        "1": interface_configuration,
        "2": default_execution
    }
    try:
        handler_function = handler.get(case_key,default_execution)          ##handler_function is reference to original function which is assigned by .get method
        result = handler_function(*args) if args else handler_function()    
        return result        
    
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

##Configure_interface
def configure_interfaces(*args):
    netmiko_connection = args[0]            ##unwrap the tupple
    menu_items = ["Interfaces Configuration","Exit"]
    try:
        interface_result= netmiko_connection.send_command("show ip interface brief",use_textfsm=True)
        configuration_menu(menu_items)                  ##Getting the output
        case_key = input("Enter your choice:- ")
        result = dynamic_match(case_key,interface_result,netmiko_connection)
        return result                ##this is the result of the function
    
    except ValueError as value:
        print(Text_File.exception_text["value_error"],value)

    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)


# ##Main function calls here 
def main(*args, **kwargs):
    return configure_interfaces(*args, **kwargs)

# ##calling the main function
if __name__ == "__main__":
    result = main()  # Call the main function
