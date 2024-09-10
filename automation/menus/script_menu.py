## Importing required Modules
import os
import importlib.util
from assets.text_file import Text_File
from datetime import datetime
from time import time

##Script Menu Class
class ScriptMenu:
    def __init__(self, menu_utils) -> None:
        self.menu_utils = menu_utils
        self.script_action = self.load_script_actions()
        self.menu_items = self.menu_items_list()
        self.cisco_script_path = self.cisco_script_path()

    def cisco_script_path(self):                ##Script Path Specifier
        current_dir = os.path.dirname(os.path.abspath(__name__))            ##Absolute Path declaration
        print(f"_____________> {current_dir} _____________<")
        relative_path = "automation\scripts\cisco_script" if os.name =="nt" else "automation/scripts/cisco_script"       ##
        result = os.path.join(current_dir, relative_path)
        return result

    def menu_items_list(self) -> list:              ##menu items list
        exclude_items = {"__init__.py", "unwanted_file.py", "__pycache__"}
        dir_list = [item.strip(".py") for item in os.listdir(self.cisco_script_path()) if item not in exclude_items]
        print(f"Menu items: {dir_list}")  # Debugging statement
        return dir_list

    def load_script_actions(self) -> dict:              ##load script action menu return
        menu_items = self.menu_items_list()
        items_sequence = len(menu_items)
        print(f"Menu items for actions: {menu_items}")  # Debugging statement
        return {str(i + 1): self.create_script_action(menu_items[i]) for i in range(items_sequence)}                

    def create_script_action(self, script_name: str): 
        def action(*args, **kwargs):
            module = self.import_module(script_name)                ##Problem occur statement
            print(f"--------->This is the module of the function {module} <-------------")
            if module:
                func = getattr(module, 'main', None)            ##getattr function boject "main"            
                print(f"Name of the function:- --------> {func} <---------")
                if func and callable(func):
                    try:                
                        print(f"Calling {script_name}.main with args={args} kwargs={kwargs}")           
                        result = func(*args, **kwargs)                          ##Connect handler netmiko (""deive_, device_typew, username ) -> Object
                        print(f"Result of {script_name}.main: {result}")
                        return result
                    except TypeError as e:
                        print(f"Error calling {script_name}.main with args={args} kwargs={kwargs}: {e}")
                else:
                    print(f"Function `main` not found in {script_name}")
                    return None
            return False
        return action

    ##Module import method
    def import_module(self, script_name):           ##Resolved path variable issue 
        module_path = os.path.join(self.cisco_script_path, f"{script_name}.py")
        if not os.path.isfile(module_path):
            print(f"Module {script_name} does not exist.")
            return None
        spec = importlib.util.spec_from_file_location(script_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    ##File creation method
    @staticmethod
    def __file_creation(File_name:str,data__:str)->bool:
        try:
            ts = time()         ##Method to get the current time
            current_dir = os.path.dirname(os.path.abspath(__name__))
            basepath = "result"                                         ##Base path for the for the file outcome
            file_path = os.path.join(current_dir,basepath)
            filename = f"{File_name}_{datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')}.txt"
            file_location = file_path + "/" + filename
            with open(file_location,"w") as f:
                if f.write(data__):
                    print(Text_File.common_text["Successful_File_Creation"])
                    return True
                else:
                    print(Text_File.error_text["Unsuccessful_File_Creation"]) 
                    return False
                
        except FileNotFoundError as fileerror:
            print(Text_File.exception_text["file_not_found"],fileerror)
        
        except Exception as e:
            print(Text_File.exception_text["common_function_exception"])
    
    ##Result hanlder()
    def result_handler(self,result):
        try:
            file_choice = input(Text_File.common_text["File_save_permission"]).strip().lower()    
            if file_choice == "yes":            
                self.__file_creation(File_name="File_Output",data__=result)
            exit_permission = input(Text_File.common_text["Exit_Permission"]).strip().lower()
            if exit_permission == "yes":
                return True
        except ValueError as value:
            print(Text_File.exception_text["value_error"],value)
            return False
        
        except Exception as e:
            print(Text_File.exception_text["common_function_exception"],e)
            return False


    def script_display_menu(self, connection):  # Accept connection as parameter
        while True:
            self.menu_utils.display_menu(self.menu_items)
            user_choice = self.menu_utils.get_user_choice(self.script_action)
            action = self.script_action.get(user_choice)            ##Dynamically generate function object
            if action:
                print(f"This is action output {action} <<<<<<<<<")
                print(f"Executing action for choice: {user_choice}")  # Debug statement
                result = action(connection)
                output = self.result_handler(result)                 ##Calling the handler to manage the result
                if output != True:
                    pass
                else:
                    break
        self.navigation.display()           ##Going to main Menu
                
                    
            
            
                