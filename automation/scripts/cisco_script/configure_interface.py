import typing
from assets.text_file import Text_File

def configure_interfaces(*args, **kwargs):
    netmiko_connection = args[0]            ##unwrap the tupple
    try:
        result= netmiko_connection.send_command("show ip interface brief", strip_prompt=False, strip_command=False)
        print(f"This is your result {result}")
        user_choice = input("Do you want to make any changes from the above outout (Yes/No):-").strip().lower()
        if user_choice == "yes":
            print("(1)Want to make interface UP")
            print("(2)Want to make assign the IP Addresss")
            print("(3)Want to update some thing")
            user_input = int(input("Enter your choice:- "))
            match user_input:
                case 1:
                    print("Which interface you want to up")
                case 2:
                    print("Which interface you want to assign the IP Address")
                case 3:
                    print("Do you want to update something")
                case _:
                    print("You have selected the wrong choice")

        else:
            print("We can;t perform the changes")

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
