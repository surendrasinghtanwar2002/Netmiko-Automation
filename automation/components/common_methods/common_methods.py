import json
from assets.text_file import Text_File
from assets.text_style import Text_Style

class Common_Methods(Text_Style):
    def __init__(self,netmiko_connection:object) -> None:
        self.netmiko_connection = netmiko_connection
    
    def configuration_menu(self,menu_items:list)->None:
        """
        The method configuration menu is used to display the configuration menu items on the screen \n
        Arguments:- 
                    (1) menu_items -> List
        """
        try:
            for item_no,item_value in enumerate(menu_items,start=1):
                self.common_text(primary_text=f"({item_no}) {item_value}")
        except ValueError as value:
            self.common_text(primary_text=Text_File.exception_text["value_error"],secondary_text=value)
            return False
        except Exception as e:
            self.common_text(primary_text=Text_File.exception_text["common_function_exception"],secondary_text=f"{__name__} {e}")
            return False

    def Interface_details(self, interface_details:dict)->None:
        """
        The method Interface details is used to display the details of device interface \n
        Arguments:- 
                    (1)interface_details -> dict
        """
        try:
            user_input = input(self.common_text(primary_text=Text_File.common_text["interface_details"])).strip().lower()
            if user_input == "yes":
                self.common_text(primary_text=Text_File.common_text["show_interface_details"],primary_text_color="yellow",secondary_text=f"\n{interface_details}",secondary_text_color="green")
                return interface_details
        except Exception as e:
            self.common_text(primary_text=Text_File.exception_text["common_function_exception"],secondary_text=e)
            return False
        
    def Data_convertor(self,raw_data:str,indentation:int=4):
        """
        The method Json_String_Convertor is used to convert the raw data into Json data \n
        Arguments:-
                    (1) raw_Data -> str
                    (2) indentation -> int
        """
        menu_items = ["Json String to a Python object","Python object to a Json String","Exit"]
        try:
            self.configuration_menu(menu_items=menu_items)
            counter_value = 1
            max_value = 3
            while counter_value < max_value:
                user_choice =input(self.common_text(primary_text=Text_File.common_text["user_choice_no"])).strip()
                match user_choice:
                    case 1:                 ##JSON String to Python object
                        self.common_text(primary_text=Text_File.common_text["json_to_python_object"],primary_text_color="yellow")
                        print("We will perform the json string to python object")
                        if isinstance(raw_data,str):
                            python_object = json.loads(raw_data)
                            return python_object
                        else:
                            counter_value += 1          #-> Increasing counter by 1
                            print("Your given  data is not in json string please check it again")          
                    case 2:                 ##Python object to Json String
                        print("We will convert python object to a string object")
                        if isinstance(raw_data,dict):
                            json_string = json.dumps(raw_data,indent=indentation)
                            return json_string
                        else:
                            counter_value += 1          #->Increasing counter by 1
                            print("Your given data is not in python object so please check it again")
                    case 3:
                        return False;
                    case _:
                        print("Please select a proper option from the above list")
        except Exception as e:
            print("We will get the exception of the function",e)
