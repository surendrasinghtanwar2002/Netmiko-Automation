from assets.text_file import Text_File

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

##Get Interface Details
def interface_configuration():
    try:
        print("Get Interface Details")
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)
        return False

def default_execution():
    try:
        print("Handle the Default statement")
        return False
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"],e)

def dynamic_match(case_key,*args):
    handler = {
        "1": interface_details,
        "2": interface_configuration,
        "3": default_execution
    }
    try:
        handler_function = handler.get(case_key,default_execution)          ##handler_function is reference to original function which is assigned by .get method
        result = handler_function(*args) if args else handler_function()    
        return result        
    
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"])
        

##main function
def main():
    configuration_menu()
    dynamic_match()

#calling the main function
if __name__ =="__main__":
    main()