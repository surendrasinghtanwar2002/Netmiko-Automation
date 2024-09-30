from .main_menu import Main_Menu
from state.global_State_Manger import Global_State_Manager
from assets.text_file import Text_File
import importlib.util
import shutil
import os

class Script_Menu(Main_Menu):
    def __init__(self,menu_items=None, event_handlers=None) -> None:
        self.menu_items = self.__menu_items_list()
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
        # print(f"Menu items: {Global_State_Manager.Single_Device}")  # Debugging statement
        return dir_list
    
    ##Method for creating a event handler dictionary from the create script actions
    def __load_script_actions(self) -> dict:              ##load script action menu return
        menu_items = self.__menu_items_list()
        items_sequence = len(menu_items)
        return {str(i + 1): self.__create_script_action(script_name=menu_items[i]) for i in range(items_sequence)} 
    
    ##Method for creating the script action and loading module dynamically using the importlib.util module
    def __create_script_action(self, script_name: str): 
        def action(connection):
            module_path = os.path.join(self.__cisco_script_path, f"{script_name}.py")   
            spec = importlib.util.spec_from_file_location(script_name, module_path)
            module = importlib.util.module_from_spec(spec)   ##This method is creating a new module object
            spec.loader.exec_module(module)                            
            if module:
                func = getattr(module, 'main', None)            ##getattr function boject "main"            
                if func and callable(func):
                    try:                
                        result = func(connection)               
                        return result
                    except TypeError as e:
                        print("Error calling here",e)
                else:
                    print(f"Function `main` not found in {script_name}")
                    return None
            return False
        return action
    
    ##Overiding the main menu of the parent menus
    def display_main_menu(self,netmiko_type:object | list) -> None:
        try:
            while True:
                self.clear_screen()
                if isinstance(netmiko_type,object):
                    self.common_text(primary_text=f"{Text_File.common_text["Device_connection_details"]}{netmiko_type.host} ".center(shutil.get_terminal_size().columns,"#"),primary_text_color="green",primary_text_style="bold")
                self.render_menu_items(menu_items=self.menu_items)
                choicevalue = self.check_user_choice()
                if choicevalue:
                    action = self.script_event_hanlders.get(choicevalue)(self)
                    if action:
                        result = action(netmiko_type)
                        print(f"This is your result {result}")
                        break
        except Exception as e:
            print(f"This is the exception of the function {e}")
                
    def debugger(self):
        print("Hey bro whatsupp ")
            
        
        
        
        
        
        
        
        
        