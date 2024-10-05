from typing import Any
from components.common_decorator.common_decorator import Regular_Exception_Handler
from automation.menus.main_menu import Main_Menu
from automation.components.command_dispatcher.command_controller import Command_Controller
from assets.text_file import Text_File

class ConfigureVlan(Main_Menu,Command_Controller):
    def __init__(self) -> None:
        self.vlan_netmiko_connection = None              #It will hold the netmiko connection object
        self.Configure_Vlan_Menu_Item = ["Show Vlan","Add Vlan","Delete Vlan","Exit"]
        self.Configure_Vlan_Event_Handler = {
            "1": self.showvlan,
            "2": self.Add_Vlan,
            "3": self.exit_menu
            }
        
        Main_Menu.__init__(self,menu_items=self.Configure_Vlan_Menu_Item,event_handlers=True)                   ##Calling constructor of Main Menu Class
        Command_Controller.__init__(self,netmiko_connection=self.vlan_netmiko_connection)      

    @Regular_Exception_Handler              
    def showvlan(self):
        result = self.manage_connection_execution(command="show vlan brief")
        if result:
            self.common_text(primary_text=Text_File.common_text["Command_ouput_message"],secondary_text=result)
        else:
            self.ExceptionTextFormatter(primary_text=Text_File.common_text["unsuccesful_command_execution"])
    

    @Regular_Exception_Handler
    def __Single_Vlan(self):
        user_vlan_choice = int(input(self.common_text(primary_text=Text_File.common_text["vlan_interface"])).strip())
        command = f"vlan {user_vlan_choice}"
        if user_vlan_choice:
            result = self.manage_connection_execution(command=command,configuration_command=True)
            if result:
                print(f"We have configure the vlan succesfully:- {result}")
            else:
                print(f"We are not able to configure the vlan succesfully")

    @Regular_Exception_Handler
    def Add_Vlan(self):
        user_choice = int(input(self.common_text(primary_text=Text_File.common_text["vlan_create_range"])).strip())
        if user_choice and user_choice == 1:
            self.__Single_Vlan()
        elif user_choice and user_choice == 2:
            print("we will do nothing on the device")
    
    @Regular_Exception_Handler
    def Delete_Vlan(self):
        print("In this section we will delete the vlan")
        
    def __call__(self,connection) -> Any:           ##Callable object
        self.vlan_netmiko_connection = connection
        self.display_main_menu()