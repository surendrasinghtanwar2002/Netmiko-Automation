from assets.text_file import Text_File
from assets.text_style import Text_Style
from assets.patterns_collection import basic_user_prompt, error_prompt_handling
from components.common_decorator.common_decorator import Regular_Exception_Handler
import re
import sys

class Prompt_Manager(Text_Style):
    def __init__(self, command: str, command_output: str) -> None:
        self.command = command
        self.command_output = command_output

    @Regular_Exception_Handler
    def BasicPromptHandler(self):
        """
        Searches for a matching user prompt in the command output.

        Returns the corresponding response if a match is found; otherwise, displays an error message.
        """
        for user_prompt, response in basic_user_prompt.items():
            if re.search(user_prompt, self.command_output):
                self.common_text(primary_text=Text_File.common_text["succesful_found_prompt"],
                                 primary_text_color="yellow",
                                 secondary_text=user_prompt,
                                 secondary_text_color="green")
                return response
        self.common_text(primary_text=Text_File.error_text["unsuccesful_prompt"],
                         primary_text_color="red")
        return False

    @Regular_Exception_Handler
    def errorprompthandler(self):
        """
        Checks for error prompts in the command output.

        Returns True if an error pattern is found; otherwise, displays an error message and returns False.
        """
        for key, pattern in error_prompt_handling.items():
            if re.search(pattern, self.command_output, re.MULTILINE):
                self.common_text(primary_text=Text_File.common_text["succesful_found_prompt"],
                                 primary_text_color="yellow",
                                 secondary_text=pattern,
                                 secondary_text_color="green")
                return True
        self.common_text(primary_text=Text_File.error_text["unsuccesful_prompt"],
                         primary_text_color="red")
        return False

    def demo(self):
        print("DEMO FUNCTION: Performing a demo task...")

    def demo1(self):
        print("DEMO FUNCTION: Running another demo task...")

    def demo2(self):
        print("DEMO FUNCTION: Executing demo task 2...")

    def PromptNavigator(self):
        """
        Executes a series of prompt handling methods in sequence.

        Iterates through a list of methods, calling each one dynamically. If an error is detected
        by `errorprompthandler`, prompts the user for input on whether to continue or exit. 
        Returns the result of the first successful method. If no method returns a valid result, 
        the function returns None.
        """
        # List of methods to be executed
        methods_to_call = [self.BasicPromptHandler, self.errorprompthandler, self.demo, self.demo1, self.demo2]

        for method in methods_to_call:
            result = method()  # Dynamically call the method

            # If the method is errorprompthandler and it returns True
            if method == self.errorprompthandler and result:
                print(f"Error detected for command: {self.command}")
                user_choice = input("An error occurred. Do you want to continue (yes/no)? ").strip().lower()

                if user_choice == "no":
                    sys.exit(self.common_text(primary_text=Text_File.common_text["greeting_user"],
                                              primary_text_color="green",
                                              primary_text_style="italic",
                                              add_line_break=False))
                else:
                    print("Continuing to the next step...")

            # If a valid result is found from other methods
            if result:
                print(f"Result from {method.__name__}: {result}")
                return result

        # If no valid result found, return None or handle it another way
        return False

       
        


        

