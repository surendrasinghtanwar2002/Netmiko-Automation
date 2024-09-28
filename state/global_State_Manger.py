from typing import Any

##Global Class State Manager
class Global_State_Manager:
    Single_Device = None
    Multiple_Device = None

    '''This class is create for managing the state of netmiko device Globally
       
       Two class Methods are being created:- 
       (1)Netmiko State Push Manager()
       (2)Netmiko State Pop Manager()
    '''
    @classmethod
    def Netmiko_State_Push_Manager(cls,device:Any):
        if isinstance(device,list):                     
            if len(device) == 1:
                cls.Single_Device = device                  ##If single device object occur
                return cls.Single_Device
            elif len(device) >  1 :    
                cls.Multiple_Device = device                ##If multiple device object occur in the list
                return cls.Single_Device
        else:
            cls.Single_Device = device                      ##When items is not in the list 
            return cls.Single_Device
        return False                                        ##Return Flase if no of above condition will match
    
    @classmethod
    def Netmiko_State_Pop_Manager(cls, value: int):
        if value == 1 and cls.Single_Device:
            cls.Single_Device.disconnect()
            cls.Single_Device = None  # Clear after disconnecting
            return True
        elif value > 1 and cls.Multiple_Device:
            for connection in cls.Multiple_Device:
                connection.disconnect()
            cls.Multiple_Device = None  # Clear after disconnecting
            return True
        return False



