from assets.text_file import Text_File
from assets.text_style import Text_Style
from state.global_State_Manger import Global_State_Manager
from concurrent.futures import ThreadPoolExecutor
from components.common_decorator.common_decorator import Regular_Exception_Handler,ThreadPoolExeceptionHandler,NetmikoException_Handler
import time

class Command_Controller(Text_Style):
    def __init__(self,netmiko_connection:str | list, commands: str | list) -> None:
        self.netmiko_connection = netmiko_connection
        self.commands = commands
        self.device_backup = None           ##By default device_backup is empty
        self.backup_command = "show running-config"

    @ThreadPoolExeceptionHandler
    def execute_with_control(self):
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
        final_result = " "              ##Final result for the multiple commands
        if isinstance(self.commands,str):
            command_result = self.netmiko_connection.send_command(self.commands)
            return command_result
        elif isinstance(self.commands,list):
            for command in self.commands:
                command_result = self.netmiko_connection.send_command(command)
                final_result += command_result + "\n"
            return final_result
        else:
            return False
        
    @Regular_Exception_Handler
    def manage_connection_execution(self):
        if isinstance(self.netmiko_connection,object):
            command_response = self.send_command()
            if command_response:
                return command_response
            else:
                return False
            
        elif isinstance(self.netmiko_connection,list):
            command_response = self.execute_with_control()
            if command_response:
                return command_response
            else:
                return False
    
    @Regular_Exception_Handler
    def write_backup_configuration(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        final_final_name = f"Today Backup {timestr}"
        with(final_final_name,"w") as file:
            if file.write(self.device_backup):
                Text_Style.common_text(primary_text=Text_File.common_text["Successful_File_Creation"])
                return True
            else:
                Text_Style.common_text(primary_text=Text_File.error_text["Failed_File_Creation"])
                return False

    @NetmikoException_Handler
    def generate_config_backup(self):
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




    
    
        

        

        