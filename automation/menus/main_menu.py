import sys
import shutil
import os
from time import time
from assets.text_file import Text_File
from assets.text_style import Text_Style

class Main_Menu(Text_Style):
    def __init__(self, menu_items=None, event_handlers=None) -> None:
        self.menu_items = menu_items if menu_items else ["Cisco", "Juniper", "Arista", "Exit"]
        self.event_handlers = event_handlers if event_handlers else {
            "1": self.cisco_devices,
            "2": self.juniper_devices,
            "3": self.arista_devices,
            "4": self.exit_menu         
        }
    @staticmethod
    def _clear_screen() -> None:
        try:
            os.system("cls" if os.name == "nt" else "clear")
        except OSError as oserror:
            Text_Style.common_text(primary_text=Text_File.exception_text["os exception"],error_text=oserror)
        except Exception as e:
            print(f"Common Exception {e}")

    def _timeexecution(original_function):                                  ##Now this decorator should be seperate in the class
        def wrapper(*args, **kwargs):
            try:
                start_time = time()
                result = original_function(*args, **kwargs)
                end_time = time()
                print(f"Function {original_function.__name__} executed in {end_time - start_time:.2f} seconds")
                return result
            except TypeError as type_error:
                print(f"Type Error {type_error} in function {original_function.__name__}")
            except Exception as e:
                print(f"Common Exception {e} in function {original_function.__name__}")
        return wrapper

    @staticmethod
    def __next_screen() -> None:
        try:
            from .connection_type_menu import Connection_type_menu
            next_display = Connection_type_menu()
            next_display.display_main_menu()
        except FileNotFoundError as file_error:
            print(f'Function: {__name__}, Exception: {type(file_error).__name__}')

    @_timeexecution
    def cisco_devices(self) -> None:
        print("Wait a minute we are landing you to Cisco devices main page")
        self.__next_screen()

    @_timeexecution
    def juniper_devices(self) -> None:
        print("Be available soon")
        self.__next_screen()

    @_timeexecution
    def arista_devices(self) -> None:
        print("Be available soon")
        self.__next_screen()

    @_timeexecution
    def exit_menu(self) -> None:
        user_choice = input("Do you want to quit (Yes/No):-").strip().lower()
        if user_choice == "yes":
            sys.exit("Thank you for using the Netmiko Automation Script".center(shutil.get_terminal_size().columns, "!"))
        else:
            pass

    @_timeexecution
    def __render_menu_items(self,menu_items:list) -> None:
        for seq_no, item in enumerate(menu_items, start=1):
            print(f"({seq_no}) {item}")

    @_timeexecution
    def _check_user_choice(self) -> None:
        user_choice = input("Enter your choice from the above menu:- ").strip()
        if user_choice in self.event_handlers:
            return user_choice
        else:
            print("Your given input is not presented in the menu")

    @_timeexecution
    def display_main_menu(self) -> None:
        self._clear_screen()
        while True:
            self.__render_menu_items(menu_items=self.menu_items)
            choice_value = self._check_user_choice()
            if choice_value:
                self.event_handlers.get(choice_value)()
                break
            else:
                print("You have given the wrong value here")

def main():
    obj = Main_Menu()
    obj.display_main_menu()

if __name__ == "__main__":
    main()
