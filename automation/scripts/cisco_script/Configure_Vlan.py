from typing import Any
from assets.text_file import Text_File
import components.common_methods.common_methods as common_methods
import menus.main_menu as menuitems

Main_Menu = menuitems.Main_Menu
Common_Methods = common_methods.Common_Methods
class Configure_Vlan(Main_Menu,Common_Methods):
    def __init__(self) -> None:
        self.netmiko_connection = None
        self.Vlan_Menu_Items = ["Show Vlan Brief","Configure Vlan","Exit"]  
        self.Vlan_event_handlers= {"1":self.configure_vlan,
                                   "2":self.showvlan_details,
                                   "3":self.exit_menu
                                   }         
        ##Passing the value to the super class   
        Main_Menu.__init__(menu_items=self.Vlan_Menu_Items,event_handlers=self.Vlan_event_handlers)       ##Passing netmiko connection object to the super class (Main Menu)
        Common_Methods.__init__(netmiko_connection=self.netmiko_connection)                               ##Passing netmiko connection object to the super class (Common methods)
    
    def showvlan_details(self):
        try:
            print("VLAN DETAILS ARE PRINTING AROUND")
        except Exception as e:
            print(f"This is the exception from the configure vlan menu item",e)

    def configure_vlan(self):
        try:
            print("Configuring vlan details")
        except Exception as e:
            print(f"This is the exception of the function")

    def Configure_Vlan_Menu(self):
        """
        Configure Vlan Menu is the method to render the menu of Vlan Menu
        """
        self.clear_screen()
        self.display_main_menu()
        if isinstance(self.netmiko_connection,object):
            result = self.commands_send(command="show ip interface brief",device=self.netmiko_connection)
            print(result)
        elif isinstance(self.netmiko_connection,list):
            output = self.parallelDeviceCommand(device_list=self.netmiko_connection,command_list="show ip interface brief")
            print(output)
    
    def __call__(self,connection) -> Any:           ##Callable object
        self.netmiko_connection = connection
        self.Configure_Vlan_Menu()