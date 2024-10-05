from typing import Any
from assets.text_file import Text_File

class Show_Calendar:
    def __init__(self):
        self.vlan_netmiko_connection = None

    def display(self):
        return f"This is your netmiko object here {self.vlan_netmiko_connection}"        

    def __call__(self, connection) -> Any:
        print(connection)
        return 10+20