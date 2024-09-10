import os
import platform
from typing import List

class MenuUtils:
    def __init__(self) -> None:
        # The constructor is not required now
        pass

    def clear(self)->None:
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    def display_menu(self, menu_items:List[str])->None:
        try:
            self.clear()     
            for index, item in enumerate(menu_items, start=1):
                print(f"({index}) {item}")
        except ValueError as valueerror:
            print("Value error:", valueerror)
        except Exception as error:
            print("An error occurred:", error)

    def get_user_choice(self, menu_actions:dict)->None:
        try:
            while True:
                choice = input("Enter your choice: ")
                if choice in menu_actions:
                    return choice
                print(f"Invalid choice. Please enter a number between 1 and {len(menu_actions)}.")
        except ValueError as valuerror:
            print("Value error:", valuerror)
        except Exception as error:
            print("An error occurred:", error)

