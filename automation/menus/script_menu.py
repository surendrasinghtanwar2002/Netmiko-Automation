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
        relative_path = "automation\scripts\cisco_script" if os.name =="nt" else "automation/scripts/cisco_script"       
        result = os.path.join(current_dir, relative_path)
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
        return {str(i + 1): self.__create_script_action(script_name=menu_items[i], class_name=menu_items[i].capitalize()) for i in range(items_sequence)}
        
    
    ##Method for creating the script action and loading module dynamically using the importlib.util module
    def __create_script_action(self, script_name: str, class_name: str):
        def action(connection):
            module_path = os.path.join(self.__cisco_script_path, f"{script_name}.py")
            spec = importlib.util.spec_from_file_location(script_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if module:
                # Dynamically load the class from the module
                class_ = getattr(module, class_name, None)
                if class_:
                    # Creating a instance from the class
                    class_instance = class_()

                    # If the class has a __call__ method, invoke it directly
                    if callable(class_instance):
                        try:
                            result = class_instance(connection)
                            return result
                        except TypeError as e:
                            self.common_text(primary_text=Text_File.common_text["instance_error"],secondary_text=e)
                    else:
                        self.common_text
                        self.common_text(primary_text=class_name,secondary_text=Text_File.error_text["callable_error"])
                else:
                    self.common_text(primary_text=f"Class {class_name} not found in the module",secondary_text=script_name)
            return False
        return action
    
    ##Overiding the main menu of the parent menus
    def display_main_menu(self,netmiko_type:object | list) -> None:
        try:
            self.netmiko_connection = netmiko_type          ##passing the netmiko object to instance variable
            while True:
                self.clear_screen()
                if isinstance(self.netmiko_connection,object):
                    self.common_text(primary_text=f"{Text_File.common_text["Device_connection_details"]}{netmiko_type.host} ".center(shutil.get_terminal_size().columns,"#"),primary_text_color="green",primary_text_style="bold")
                self.render_menu_items(menu_items=self.menu_items)
                choicevalue = self.check_user_choice()
                if choicevalue:
                    action = self.script_event_hanlders.get(choicevalue)(self)
                    if action:
                        result = action(self.netmiko_connection)
                        print(f"In this are we will get the result from the class menu and further we can perform any task here:---- {result}")        ##Just used for debugging purpose
                        break
        except Exception as e:
            self.common_text(primary_text=Text_File.exception_text["common_function_exception"],secondary_text=e)
                
            
        
        
        
        
        
        
        
        
        