from typing import Any
from assets.text_file import Text_File

class Show_Calendar:
    def __init__(self):
        self.vlan_netmiko_connection = None

    def display(self):
        user_choice = input("Enter your prompt here to continue the process:- ")
        if  user_choice:
            print("We are working well on this project")
        return f"This is your netmiko object here {self.vlan_netmiko_connection}"        

    def __call__(self, connection) -> Any:
        self.vlan_netmiko_connection = connection
        result = self.display()
        if result:
            return result
        else:
            return False