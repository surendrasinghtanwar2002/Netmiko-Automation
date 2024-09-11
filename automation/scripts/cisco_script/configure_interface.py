from assets.text_file import Text_File
from automation.scripts.configuration_menu.configuration_menu import configuration_menu,dynamic_match

def configure_interfaces(*args, **kwargs):
    netmiko_connection = args[0]            ##unwrap the tupple
    menu_items = ["Get Interface Details","Interfaces Configuration","Exit"]
    try:
        interface_result= netmiko_connection.send_command("show ip interface brief",use_textfsm=True)
        user_choice = input("Do you want to make any changes from the above outout (Yes/No):-").strip().lower()
        if user_choice == "yes":
            configuration_menu(menu_items)                  ##Getting the output
            case_key = input("Enter your choice:- ")
            result = dynamic_match(case_key,interface_result,netmiko_connection)
            return result                ##this is the result of the function
        else:
            print("We can't perform the changes")

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
