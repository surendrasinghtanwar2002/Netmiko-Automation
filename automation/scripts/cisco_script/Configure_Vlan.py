from typing import Any
from assets.text_file import Text_File
import components.common_methods.common_methods as common_methods
import menus.main_menu as menuitems

Main_Menu = menuitems.Main_Menu
Common_Methods = common_methods.Common_Methods
class Configure_Vlan(Main_Menu,Common_Methods):
    def __init__(self) -> None:
        self.netmiko_connection = None
        self.Vlan_Menu_Items = ["Show Vlan Brief","Configure Vlan","Create Vlan","Delete Vlan","Exit"]  
        self.Vlan_event_handlers= {"1":self.showvlan_details,
                                   "2":self.configure_vlan,
                                   "3":self.Create_Vlan,
                                   "4":self.Delete_Vlan,
                                   "4":self.exit_menu
                                   }         
        ##Passing the value to the super class   
        Main_Menu.__init__(menu_items=self.Vlan_Menu_Items,event_handlers=self.Vlan_event_handlers)       ##Passing netmiko connection object to the super class (Main Menu)
        Common_Methods.__init__(netmiko_connection=self.netmiko_connection)                               ##Passing netmiko connection object to the super class (Common methods)
    
    def showvlan_details(self):
        """
        Fetch and display VLAN details from the network device.

        This method sends the command 'show vlan brief' to the connected network device using 
        Netmiko and retrieves VLAN information in a structured format. It utilizes TextFSM 
        for parsing the command output. The VLAN details are then displayed in a tabular format 
        using the 'display_table' method.

        Returns:
            None: The method does not return any value. It prints the VLAN details directly to the console 
            using the 'display_table' method. If no data is returned, a message is printed to indicate 
            the absence of VLAN information.

        Raises:
            Exception: If an error occurs during command execution or data retrieval, 
            an exception message is printed to the console, indicating the source of the error.
        """
        try:
            vlan_details = self.netmiko_connection.send_command("show vlan brief", use_textfsm=True)
            if vlan_details:
                table_data = []
                for data in vlan_details:
                    row = [data.get("vlan_id"),
                        data.get("name"),
                        data.get("status"),
                        data.get("ports"),
                        ]
                    table_data.append(row)
                self.display_table(data=table_data, headers=["Vlan_Id", "Vlan Name", "Vlan Status", "Vlan Ports"])
            else:
                print("Not returned anything still working on that")
                return False
        except Exception as e:
            print(f"This is the exception from the show vlan details menu item", e)

    def Create_Vlan(self):
        try:
            user_choice = int(input("Enter your number of vlan you want to create:- ").strip())
            if user_choice:
                for vlan_no in user_choice+1:
                    commands = [f"vlan {vlan_no}",f"name Netmikoscriptvlan {vlan_no}"]
                    result = self.commands_send(command=commands,configuration=True)
                print(result)
            else:
                print("Please choose a proper option")    
                
        except Exception as e:
            print(f"This is the exception of the function {e}")
    
    def Delete_Vlan(self):
        try:
            print("In this section we will delete the ")
        except Exception as e:
            print("In this section we will delete the vlan")

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
    
    def __call__(self,connection) -> Any:           ##Callable object
        self.netmiko_connection = connection
        self.Configure_Vlan_Menu()