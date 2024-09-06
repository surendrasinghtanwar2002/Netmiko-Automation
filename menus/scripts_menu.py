import os
import importlib.util

class ScriptMenu:
    def __init__(self) -> None:
        # self.connection_type_menu_instance = self.connection_type_menu_instance
        self.script_action = self.load_script_actions()
        self.menu_item = self.menu_items_list()

    def menu_items_list(self) -> list:
        path = "/Users/surendrasingh/Desktop/Netmiko-Automation/scripts/cisco_script"
        exclude_items = {"__init__.py", "unwanted_file.py"}
        dir_list = [item.strip(".py") for item in os.listdir(path) if item not in exclude_items]
        print(f"Menu items: {dir_list}")  # debugging statement
        return dir_list

    def load_script_actions(self):
        menu_items = self.menu_items_list()
        items_sequence = len(menu_items)
        print(f"Menu items for actions: {menu_items}")  # debugging statement
        return {str(i + 1): self.create_script_action(menu_items[i]) for i in range(items_sequence)}

    def create_script_action(self, script_name):
        def action():
            module = self.import_module(script_name)
            if module:
                func = getattr(module, 'main', None)
                if func and callable(func):
                    func()
                    return True
                else:
                    print(f"Function `main` not found in {script_name}")
            return False

        return action

    def import_module(self, script_name):
        path = "/Users/surendrasingh/Desktop/Netmiko-Automation/scripts/cisco_script"
        module_path = os.path.join(path, f"{script_name}.py")

        if not os.path.isfile(module_path):
            print(f"Module {script_name} does not exist.")
            return None

        spec = importlib.util.spec_from_file_location(script_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def script_display_menu(self):
        while True:
            from menu_utils import display_menu, get_user_choice
            display_menu(self.menu_item)
            user_choice = get_user_choice(self.script_action)
            action = self.script_action.get(user_choice)
            if action and action():
                break


