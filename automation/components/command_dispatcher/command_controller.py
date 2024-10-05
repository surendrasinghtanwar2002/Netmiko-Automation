from assets.text_file import Text_File
from assets.text_style import Text_Style
from state.global_State_Manger import Global_State_Manager          ##It is global statemanager and we will use if any requirement occur
from concurrent.futures import ThreadPoolExecutor
from components.common_decorator.common_decorator import Regular_Exception_Handler,ThreadPoolExeceptionHandler,NetmikoException_Handler
from components.prompt_manager.prompt_manager import Prompt_Manager
import time
import sys
import os

class Command_Controller(Prompt_Manager):
    """
    Manages the execution of commands on Netmiko connections and handles device configuration backups.

    This class supports both single and multiple Netmiko connections, enabling command execution,
    concurrent processing with threading, and backup of device configurations to timestamped files.
    """
    def __init__(self,netmiko_connection:str | list) -> None:
        self.netmiko_connection = netmiko_connection
        self.configuration = False              ## Used for making condition command is configuration command or basic command
        self.commands = None
        self.device_backup = None           ##By default device_backup is empty
        self.backup_command = "show running-config"         ##Backup command

    @ThreadPoolExeceptionHandler
    def execute_with_control(self):
        """
        Executes commands on multiple Netmiko connections concurrently using a ThreadPoolExecutor.

        If a single command string is provided, it converts it into a list for processing.
        For each connection in the Netmiko connection list, it submits the commands to the executor
        and collects the results as they complete.

        Returns:
            list: A list of results from the executed commands for each connection.
        """
        results = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            if isinstance(self.commands,str):
                commands_execute = [self.commands]              ##It will convert the command into list if a single command is being passed
            else:
                commands_execute = self.commands                ##If command is already a list so no need to convert in to the list

            for netmiko_connection in self.netmiko_connection:
                futures = [executor.submit(self.commands, netmiko_connection, command) for command in commands_execute]
                for future in futures:
                    results.append(future.result())  # Collect results as they complete
            return results

    @Regular_Exception_Handler
    def send_command(self):
        """
        Sends commands to the Netmiko connection and retrieves the results.

        If a single command string is provided, it sends that command directly.
        If a list of commands is provided, it sends each command sequentially and
        concatenates the results into a single string.

        Returns:
            str or bool: The command result(s) as a string if successful, or False if the input is invalid.
        """
        final_result = " "              ##Final result for the multiple commands
        if isinstance(self.commands,str):
            command_result = self.netmiko_connection.send_config_set(self.command) if self.configuration else self.netmiko_connection.send_command(self.commands)
            super().__init__(command,command_result)            ##passing value into super class
            result = self.PromptNavigator()
            if result:
                self.common_text(primary_text=Text_File.common_text["Your command have been succesfully performed on the server"])
                return command_result
            else:
                return False
            
        elif isinstance(self.commands,list):
            for command in self.commands:
                command_result = self.netmiko_connection.send_config_set(self.command) if self.configuration else self.netmiko_connection.send_command(self.commands)
                result = super().__init__(command,command_result)
                if result:
                    final_result += command_result + "\n"
                else:
                    self.common_text(primary_text=Text_File.common_text["Your command is not being executed succesfully"],secondary_text=command)
                    continue            ##skip and moving to the next command
            return final_result
        else:
            return False
        
    @Regular_Exception_Handler
    def manage_connection_execution(self,command:str | list,configuration_command: bool = False):              ##Main method which is calling all other method respectively
        """
        Manages the execution of commands based on the type of Netmiko connection.

        If a single Netmiko connection object is provided, it sends commands directly.
        If a list of Netmiko connections is provided, it utilizes multithreading to execute commands on all connections.

        Returns:
            list or bool: Command responses if successful, or False if execution fails.
        """
        self.command = command                  ##Passing the command to the constructor method
        self.configuration = configuration_command

        if isinstance(self.netmiko_connection,object):
            result = self.generate_config_backup()              ##This method is being used to backup the current configuration of device before making any changes
            if result:
                self.common_text(primary_text=Text_File.common_text["successful_backup"],primary_text_color="green")
            else:
                self.common_text(primary_text=Text_File.error_text["unsuccessful_backup"],primary_text_color="red")
                continue_choice = input(primary_text=Text_File.common_text["Continue_without_backup"].strip().lower())
                if continue_choice == "yes":
                    command_response = self.send_command()
                    if command_response:
                        self.common_text(primary_text=Text_File.common_text["command_excuted"],primary_text_color="green") ##Just for testing purpose we will remove final program will being made
                        return command_response
                    else:
                        self.common_text(primary_text=Text_File.common_text["error_command_excuted"],primary_text_color="red")
                        return False
                else:
                     sys.exit(self.common_text(primary_text=Text_File.common_text["greeting_user"],primary_text_color="green",primary_text_style="italic",add_line_break=False))
                    
            
        elif isinstance(self.netmiko_connection,list):
            result = self.generate_config_backup()          ##This method is being used to backup the current configuration of device before making any changes
            if result:
                 self.common_text(primary_text=Text_File.common_text["successful_backup"],primary_text_color="green")
            else:
                 self.common_text(primary_text=Text_File.error_text["unsuccessful_backup"],primary_text_color="red")
                 continue_choice = input(primary_text=Text_File.common_text["Continue_without_backup"].strip().lower())
                 if continue_choice == "yes":
                    command_response = self.execute_with_control()
                    if command_response:
                        self.common_text(primary_text=Text_File.common_text["command_excuted"],primary_text_color="green") ##Just for testing purpose we will remove final program will being made
                        return command_response
                    else:
                        self.common_text(primary_text=Text_File.common_text["error_command_excuted"],primary_text_color="red")
                        return False
                 else:
                    sys.exit(self.common_text(primary_text=Text_File.common_text["greeting_user"],primary_text_color="green",primary_text_style="italic",add_line_break=False))
    
    @Regular_Exception_Handler
    def write_backup_configuration(self):
        """
        Writes the device backup configuration to a timestamped file.
        
        The filename is generated based on the current date and time. 
        If the file is successfully created and written, a success message is displayed.
        
        Returns:
            bool: True if the file is created successfully, False otherwise.
        """
        relative_path = "device_backup"
        timestr = time.strftime("%Y%m%d-%H%M%S")
        final_file_name = f"Backup_{timestr}.txt"
        relative_path = f"device_backup/{final_file_name}"
        absolute_path = os.path.abspath(relative_path)
        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)      ##This will check either absolute path is presented or not
        with(absolute_path,"w") as file:
            if file.write(self.device_backup):
                Text_Style.common_text(primary_text=Text_File.common_text["Successful_File_Creation"])
                return True
            else:
                Text_Style.common_text(primary_text=Text_File.error_text["Failed_File_Creation"])
                return False

    @NetmikoException_Handler
    def generate_config_backup(self):
        """
        Backs up the device configuration by executing 'show running-config'.
        
        Supports both single and multiple Netmiko connections. For single devices, 
        it attempts to save the configuration up to three times if initial attempts fail. 
        For multiple devices, it uses a ThreadPoolExecutor to gather configurations concurrently.
        
        Returns:
            bool: True if the backup is successful, False otherwise.
        """
        counter = 0
        max_counter = 3
        if isinstance(self.netmiko_connection,object):                      ##Condition for single netmiko connection object
            backup_file = self.netmiko_connection.send_command("show running-config")
            if backup_file:
                self.device_backup = backup_file
                while counter < max_counter:
                    if self.write_backup_configuration():
                        return True
                    else:
                        counter += 1    ##Counter increment
                        Text_Style.common_text(secondary_text=Text_File.error_text["Failed_File_Creation"])
                        Text_Style.common_text(primary_text= Text_File.common_text["File_Creation_Again"])
                Text_Style.common_text(secondary_text=Text_File.error_text["File_Creation_Max_Limit"])      ##Message occur when max limit of loop occur
                return False
            else:
                return False
            
        elif isinstance(self.netmiko_connection,list):                  ##Condition for multiple netmiko connection object            
            final_result = " "

            backup_exectuor_command = [self.backup_command]             ##Converting the backup command into the list

            with ThreadPoolExecutor(max_workers=5) as executor:
                result = list(executor.map(self.send_command,self.netmiko_connection,backup_exectuor_command))
                if result:
                    for single_backup_device in result:
                        final_result += single_backup_device + "\n"
                    
                    self.device_backup = final_result           #Storing final result in teh device_backup 

                    while counter < max_counter:                ##A loop for the file creation
                        if self.write_backup_configuration():
                            return True
                        else:
                            counter += 1        ##Counter Increment
                        Text_Style.common_text(secondary_text=Text_File.error_text["Failed_File_Creation"])
                        Text_Style.common_text(primary_text= Text_File.common_text["File_Creation_Again"])
                    Text_Style.common_text(secondary_text=Text_File.error_text["File_Creation_Max_Limit"])      ##Message occur when max limit of loop occur
                    return False
                
                else:
                    return False
        else:
            return False            ##When above both method is not able to return anything.

    



    
    
        

        

        