import sys
import os
from time import time
from assets.text_file import Text_File
from assets.text_style import Text_Style
from automation.components.common_decorator.common_decorator import Regular_Exception_Handler

class Main_Menu(Text_Style):
    def __init__(self, menu_items=None, event_handlers=None) -> None:
        self.menu_items = menu_items if menu_items else ["Cisco", "Juniper", "Arista", "Exit"]
        self.event_handlers = event_handlers if event_handlers else {
            "1": self.__cisco_devices,
            "2": self.__juniper_devices,
            "3": self.__arista_devices,
            "4": self.exit_menu         
        }

    @Regular_Exception_Handler
    def clear_screen(self) -> None:
        """
        Clears the terminal screen based on the operating system.

        This method clears the screen by executing the appropriate system command 
        depending on whether the OS is Windows ("cls") or Unix-based ("clear"). 

        Returns:
            None
        """
        os.system("cls" if os.name == "nt" else "clear")
       
    @Regular_Exception_Handler
    def next_screen(self) -> None:
        """
        Loads and displays the connection type menu.

        This method imports the `Connection_type_menu` class to avoid circular imports,
        then renders the next menu by calling its `display_main_menu()` method.

        Returns:
            None
        """
        from .connection_type_menu import Connection_type_menu                  ##This is imported due to circular imports 
        next_display = Connection_type_menu()
        next_display.display_main_menu()
    
            
    @Regular_Exception_Handler
    def __cisco_devices(self) -> None:
        result = self.progress_bar(Progessbar_name="Loading your Next Screen")
        if result:
            self.next_screen()
        else:
            sys.exit(self.common_text(primary_text=Text_File.common_text["greeting_user"],primary_text_color="green",primary_text_style="italic",add_line_break=False))

    def __juniper_devices(self) -> None:
        result = self.progress_bar(Progessbar_name="Loading your Next Screen")
        if result:
            sys.exit(self.common_text(primary_text=Text_File.common_text["Work_in_Progress"],primary_text_color="green",primary_text_style="italic",add_line_break=False))
            sys.exit(self.common_text(primary_text=Text_File.common_text["greeting_user"],primary_text_color="green",primary_text_style="italic",add_line_break=False))
        else:
            pass

    def __arista_devices(self) -> None:
        result = self.progress_bar(Progessbar_name="Loading your Next Screen")
        if result:
            sys.exit(self.common_text(primary_text=Text_File.common_text["Work_in_Progress"],primary_text_color="green",primary_text_style="italic",add_line_break=False))
            sys.exit(self.common_text(primary_text=Text_File.common_text["greeting_user"],primary_text_color="green",primary_text_style="italic",add_line_break=False))
        else:
            pass

    @Regular_Exception_Handler
    def exit_menu(self) -> None:
        """
        Handles the exit prompt for the menu and exits the program based on user input.

        This method prompts the user with a confirmation to exit the program. If the user 
        enters "yes", the program will exit with a farewell message. Any other input will 
        cancel the exit and return to the menu.

        Returns:
            None
        """
        user_choice = input(self.common_text(primary_text=Text_File.common_text["Exit_Permission"],primary_text_color="yellow",primary_text_style="bold",add_line_break=False)).strip().lower()
        if user_choice == "yes":
            sys.exit(self.common_text(primary_text=Text_File.common_text["greeting_user"],primary_text_color="green",primary_text_style="italic",add_line_break=False))
        else:
            pass

    @Regular_Exception_Handler
    def render_menu_items(self,menu_items:list) -> None:
        """
        Renders a list of menu items with sequential numbering.

        This method takes a list of `menu_items` and displays each item with a corresponding 
        sequence number. The numbering starts at 1. Each menu item is styled with specific 
        colors and text formatting using the `common_text()` function.

        Args:
            menu_items (list): A list of strings representing the menu options.

        Returns:
            None
        """
        for seq_no, item in enumerate(menu_items, start=1):
            self.common_text(primary_text=str({seq_no}),primary_text_color="red",primary_text_style="bold",secondary_text=item,secondary_text_color="bright_cyan",secondary_text_style="bold",add_line_break=True)

    
    @Regular_Exception_Handler
    def check_user_choice(self) -> None:
        """
        Prompts the user for a menu choice and validates it.

        This method displays a prompt to the user asking for input, then checks if the input
        matches one of the valid choices stored in `self.event_handlers`. If the input is valid,
        it returns the user's choice. Otherwise, it displays an error message and does not return a value.

        Returns:
            str or None: The valid user choice if found in `self.event_handlers`, otherwise None.
        """
        user_choice = input(self.common_text(primary_text=Text_File.common_text["User_choice"],primary_text_color="blue",primary_text_style="bold",add_line_break=False)).strip()
        if user_choice in self.event_handlers:
            return user_choice
        else:
            self.ExceptionTextFormatter(primary_text=Text_File.error_text["menu_wrong_input"])

    @Regular_Exception_Handler
    def display_main_menu(self) -> None:
        """
        Displays the main menu and handles user interaction.

        This method repeatedly renders the main menu items and waits for user input.
        It checks the user's choice and invokes the corresponding event handler if a valid choice
        is made. If the choice is invalid, an error message is displayed, and the menu is rendered again.

        The method utilizes the following components:
        - `render_menu_items(menu_items)`: Renders the menu items for user selection.
        - `check_user_choice()`: Validates the user's input and returns the corresponding choice.
        - `event_handlers`: A dictionary mapping valid choices to their respective handler functions.
        - `common_text()`: Displays error messages in a specified format when the user inputs an invalid choice.

        Returns:
            None: This method does not return any value. It continues to run until a valid choice is made.
        """
        self.clear_screen()
        while True:
            self.render_menu_items(menu_items=self.menu_items)
            choice_value = self.check_user_choice()
            if choice_value:
                self.event_handlers.get(choice_value)()
                break
            else:
                self.ExceptionTextFormatter(primary_text=Text_File.error_text["wrong_value"])

