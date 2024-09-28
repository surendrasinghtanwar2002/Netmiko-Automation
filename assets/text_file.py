import shutil

class Text_File:
    def __init__(self) -> None:
        pass

    ##common text
    common_text ={
        "connection": "Connected to the host succesfully",
        "device_type":"Enter your device type (eg. cisco_ios,juniper etc....):- ",
        "connected_host":"Connected to host ",
        "print_ip_table":"Do you want to print valid ip address table (Yes/No):- ",
        "username":"Enter your Username:-",
        "password":"Enter your Password:-",
        "valid_cred":"Your credentails are in valid order",
        "host_ip_prompt":"Enter your HOST IP ADDRESS:-",
        "mutli_auth_welcome":" Welcome to Multi Device Connection Authentication Page ".center(shutil.get_terminal_size().columns,"!"),
        "same_credentials":"Do you have same credentaisl for all device (Yes/No):-",
        "range_of_ip":"Specify number of device IP Address Range eg:(1,10,15,30,45,50):-",
        "ip_address_range":"Enter Your Ip Address no",
        "validip_banner":"VALID IP ADDRESS".center(shutil.get_terminal_size().columns,"!"),
        "invalidip_banner":"INVALID IP ADDRESS".center(shutil.get_terminal_size().columns,"!"),
        "invalid_credentials":"Invalid credentials or limit reached.",
        "proceed_confirmation":"Do you want to proceed (Yes/No):-",
        "Data_retrieved":"Succesfully Data have been retrieved".center(shutil.get_terminal_size().columns,"!"),
        "Successful_File_Creation":"Your File Have been created Succesfully".center(shutil.get_terminal_size().columns,"!"),
        "File_save_permission":"Do you want to say to your file (Yes/No):- ",
        "Json_conversion_permission":"Do you want to convert raw data into json",
        "successful_state_update":"Netmiko Global State Have been updated succesfully",
        "Exit_Permission":"Do you want to exit from the menu (Yes/No):- ",
        "User_choice":"Enter your choice:- ",
        "user_choice_no":"Enter your choice (eg:- 1,2,3):-",
        "vlan_configuration_permission":"Do you want to make configuration in Vlan (Yes/No):-",
        "vlan_starting_range":"Enter your vlan starting range:-",
        "vlan_ending_range":"Enter your vlan ending range:-",
        "vlan_interface_starting":"Enter the interface range (e.g., GigabitEthernet1/0/1-5 or GigabitEthernet1/0/1):-",
        "vlan_interface":"Enter your vlan number:-",
        "Interface_Details":"From the above Interface Details Please Select Proper Range \n".center(shutil.get_terminal_size().columns),
        "vlan_create_range":"Specify your range of vlan (eg:-1,2,3,4,5,6):-",
        "vlan_no_input":"Enter Single Vlan no only (eg: 1,10,20):-",
        "vlan_no_section_banner":" You have selected ".center(shutil.get_terminal_size().columns,"*"),
        "loading_data":"We are loading the data",
        "avilable_soon":"This service is under work be avilable soon".center(shutil.get_terminal_size().columns,"*"),
        "greeting_user":" Thank you for using the netmiko script we are working every day for stable performance ".center(shutil.get_terminal_size().columns,"*"),
        "Single_device":"Single Device Connection".center(shutil.get_terminal_size().columns,"*"),
    }
    ##common text
    exception_text ={
        "common_function_exception": "Your function have exception",
        "value_error":"You have passed wrong value",
        "CalledProcessError":"Subprocess Exception occured",
        "file_not_found":"File not Founded Exception",
        "os exception":"Os exception arrived",
        "connection_failed":"Failed to connect the device"

    }
    ##error text
    error_text = {
        "device_details_error":"!!! You have provided wrong details of the device !!!".center(shutil.get_terminal_size().columns),
        "limit_exceed":"You have reached your limit",
        "Unsuccessful_File_Creation":"Your File Have not been created",
        "wrong_value":"You have provided the wrong value",
        "menu_wrong_input":"Your given input is not presented in the menu",
        "Unvalid_ip_address":"Your IP Address is not valid",
        "Device invalid":"Device is not reachable"
    }
    ##debug text
    debug_text = {
        "device_details": "We got the device details",
        "device_respond":"Device is Active".center(shutil.get_terminal_size().columns),

    }
    ##class object text
    object_text = {
        "text_style":"This Class is being used to style the text with various parameter"
    }