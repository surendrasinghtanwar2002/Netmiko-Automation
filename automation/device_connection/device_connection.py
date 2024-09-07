from typing import List
from netmiko import ConnectHandler

class device_connection:
    def __init__(self,HOST_IP_ADDRESS,USERNAME,PASSWORD,PORTNO=22) -> None:
        self.HOSTIPADDDRESS = HOST_IP_ADDRESS
        self. USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.PORTNO = PORTNO
    
    #First Method for Connecting to the device
    def single_device_connection(self):
        pass