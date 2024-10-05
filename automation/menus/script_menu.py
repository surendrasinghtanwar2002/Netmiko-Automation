from .main_menu import Main_Menu
from state.global_State_Manger import Global_State_Manager
from assets.text_file import Text_File
import importlib.util
import shutil
import os

class Script_Menu(Main_Menu):
    def __init__(self,menu_items=None, event_handlers=None) -> None:
        self.menu_items = self.__menu_items_list()
        self.netmiko_connection = None              ##This will store the netmiko object
        self.script_event_hanlders = self.__load_script_actions()
        super().__init__(menu_items=menu_items if menu_items else self.menu_items, 
                 event_handlers=event_handlers if event_handlers else self.script_event_hanlders)
    
    ##Method for getting the absolute path for the folder script
    def __cisco_script_path(self):                
        current_dir = os.path.dirname(os.path.abspath(__name__))            ##Absolute Path declaration
        relative_path = r"automation\scripts\cisco_script" if os.name == "nt" else "automation/scripts/cisco_script"
        result = os.path.join(current_dir, relative_path)
        print(f"This is your final path for the project -------------> {result} <-------------------")
        return result
    
    
    ##Method for creating menu from the oslistdir
    def __menu_items_list(self) -> list:              ##menu items list
        exclude_items = {"__init__.py", "unwanted_file.py", "__pycache__"}
        dir_list = [item.strip(".py") for item in os.listdir(self.__cisco_script_path()) if item not in exclude_items]
        return dir_list
    
    ##Method for creating a event handler dictionary from the create script actions
    def __load_script_actions(self) -> dict:              ##load script action menu return
        menu_items = self.__menu_items_list()
        items_sequence = len(menu_items)
        #assuming the class name is the capitalized version of the script name so we need to put the script name as the class name for proper configuration
        return {str(i + 1): self.__create_script_action(script_name=menu_items[i], class_name=menu_items[i]) for i in range(items_sequence)}
        
    
    ##Method for creating the script action and loading module dynamically using the importlib.util module
    def __create_script_action(self, script_name: str, class_name: str):
        def action(script_menu_instance):  # Accept the instance of Script_Menu
            print(f"This is your netmiko object passed in action button ------>{script_menu_instance.netmiko_connection} <--------------")
            print(f"-----------------------------------> This is your script name which is presented or not {script_name}")
            module_path = os.path.join(self.__cisco_script_path(), f"{script_name}.py")
            print(f"This is your module path contain the complete file path -----------> {module_path} <-------")
            spec = importlib.util.spec_from_file_location(script_name, module_path)
            print(f"Checking either module have been imported or not ----------> {spec} <----------------")
            module = importlib.util.module_from_spec(spec)
            print(f"Seeing final module is being imported or not {module}")
            spec.loader.exec_module(module)

            if module:
                print(f"----------------------------------> {module}")
                my_class = getattr(module, class_name, None)
                print(f"This is your class loaded dynamically from the module --------------->{my_class} <--------------------")
                print(f"This is your class name imported from the module {class_name}")
                if my_class:
                    class_instance = my_class()
                    print(f"This is your class instance created {class_instance}")
                    if callable(class_instance):
                        try:
                            result = class_instance(script_menu_instance.netmiko_connection)  # Pass the netmiko_connection
                            print(f"This is your result of the class instance {result}")
                            return result
                        except TypeError as e:
                            print("Type error occur")
                    else:
                        print(f"CALLABLE ERROR CLASS IS NOT BEING CALLED {class_name}")
                else:
                    print(f"Class name is not found there please check it {class_name} ")
            return False
        return action
    
    ##Overiding the main menu of the parent menus
    def display_main_menu(self,netmiko_type:object | list) -> None:
        try:
            self.clear_screen()
            self.netmiko_connection = netmiko_type          ##passing the netmiko object to instance variable
            while True:
                if isinstance(self.netmiko_connection,list):
                    for netmiko in self.netmiko_connection:
                        self.common_text(primary_text=f"{Text_File.common_text["Device_connection_details"]}{netmiko.host}".center(shutil.get_terminal_size().columns),primary_text_color="green",primary_text_style="bold")
                elif isinstance(self.netmiko_connection,object):
                    self.common_text(primary_text=f"{Text_File.common_text["Device_connection_details"]}{self.netmiko_connection.host}".center(shutil.get_terminal_size().columns,"#"),primary_text_color="green",primary_text_style="bold")
                    print(f"This is  your netmiko object passed from previous screen to next screen  {self.netmiko_connection}")
                self.render_menu_items(menu_items=self.menu_items)
                choicevalue = self.check_user_choice()
                print(f"---------------------------> {choicevalue} <----------------------------- This is choice value")
                if choicevalue:
                    action = self.script_event_hanlders.get(choicevalue)(self)
                    print(f"This is your action data {action}")
        except Exception as e:
            # self.common_text(primary_text=Text_File.exception_text["common_function_exception"],secondary_text=e)
            print("script menu exepception occured",e)
                
            
        
        
        
        
        
        
        
        
        