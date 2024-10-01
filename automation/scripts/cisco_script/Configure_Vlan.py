from typing import Any


class Configure_Vlan:
    def __init__(self) -> None:
        self.netmiko_connection = None              ##Netmiko connection object
    




    def __call__(self,connection) -> Any:           ##Callable object
        self.netmiko_connection = connection
        print(self.netmiko_connection)