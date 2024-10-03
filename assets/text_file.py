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
        "username":"Enter your Username:- ",
        "password":"Enter your Password:- ",
        "valid_cred":"Your credentails are in valid order",
        "host_ip_prompt":"Enter your HOST IP ADDRESS:- ",
        "mutli_auth_welcome":" Welcome to Multi Device Connection Authentication Page ".center(shutil.get_terminal_size().columns,"!"),
        "same_credentials":"Do you have same credentaisl for all device (Yes/No):-",
        "range_of_ip":"Specify number of device IP Address Range eg:(1,10,15,30,45,50):-",
        "ip_address_range":"Enter Your Ip Address no:- ",
        "validip_banner":"VALID IP ADDRESS".center(shutil.get_terminal_size().columns,"!"),
        "invalidip_banner":"INVALID IP ADDRESS".center(shutil.get_terminal_size().columns,"!"),
        "invalid_credentials":"Invalid credentials or limit reached.",
        "proceed_confirmation":"Do you want to proceed (Yes/No):-",
        "Data_retrieved":"Succesfully Data have been retrieved".center(shutil.get_terminal_size().columns,"!"),
        "Successful_File_Creation":"Your File Have been created Succesfully".center(shutil.get_terminal_size().columns,"!"),
        "File_save_permission":"Do you want to say to your file (Yes/No):- ",
        "Json_conversion_permission":"Do you want to convert raw data into json",
        "successful_state_update":" Netmiko Global State Have been updated succesfully ".center(shutil.get_terminal_size().columns,"!"),
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
        "Single_device":" Single Device Connection ".center(shutil.get_terminal_size().columns,"*"),
        "Work_in_Progress":"Still we are working on this be avilable soon.",
        "Multiple_Auth_Data_Range":"Please Enter your number of device you want to configure (eg:- 2,4,6,8,10):- ",
        "Multiple_connection_greeting":" Welcome to Netmiko Multiple Connection ".center(shutil.get_terminal_size().columns,"*"),
        "device_details_updated":" Your device details have been stored succesfully ".center(shutil.get_terminal_size().columns,"#"),
        "Device_connection_details":" You are connected to device  ",
        "valid_ip":"Your Ip Address is valid",
        "interface_details":"Do you want to print interface details",
        "show_interface_details":"This is your interface details",
        "json_to_python_object":"Convert the Json String to Python object",
        "object_to_json_string":"Convert the Python Object to Json String",
        "valid_option_warn":"Please choose a valid option from the menu",
        "File_Creation_Again":"File Creation process started again"
    }
    ##common exception text
    exception_text ={
        "common_function_exception": f"Your function have exception {__name__}",
        "value_error":"You have passed wrong value",
        "CalledProcessError":"Subprocess Exception occured",
        "file_not_found":f"File not Founded Exception in {__name__}",
        "os_exception":"Os exception arrived",
        "KeyboardInterrupt":"Execution was interrupted by the user. The ongoing tasks may not have completed successfully.",
        "connection_failed":"Failed to connect the device",
        "type_error":f"Type error found in the your function {__name__}",
        "progress_bar_failed":"Progress bar failed or was canceled.",
        "instance_error":"Error occured while calling the instance",
        "json_to_python_object_error":"Your given data is not Json String please check it",
        "Python_object_to_json_error":"Your give data is not Python object please check it",
        "No_valid_connector":"Netmiko have found no valid connector please check",
        "Netmiko_Timeout_Exception":"Netmiko Time exceout exception have arrived and connection is not established properly",
        "Netmiko_Base_Exception":"Netmiko Base Exception have been arrived",
        "Netmiko_Authentication_exception":"Netmiko authentication exception have been arrived connection not established",
        "ssh_exception":"Paramiko ssh exception have been arrived",
        "paramiko_auth_exception":"Paramiko auth exception have arrived connection not established succesfully",
        "Type_error":"Type error have been occrued",
        "Module_error":"Module not found please check it",
        "sub_process_exception":"The sub process module have occured a exception please check it",
        "File_Creation_Max_Limit":"We have reached our limit to create the file but file is not being created",
        "IOerror":"Error occurred while accessing the file. Please check the file path and permissions"
    }
    #threadpool module exception text
    threadpool_module_exception_text = {
        "Cancelled_Error":"The task was cancelled and cannot be completed. Please check the task status.",
        "TimeoutError":"The task has timed out. It took too long to complete. Please try again or check your network conditions.",
        "BrokenExecutor":"An error has occurred in the executor, preventing further tasks from being executed. Please restart the process.",
        "ValueError": "Invalid argument provided in ThreadPool excecutor {error}. Please check your input values and try again.",
        "TypeError": "A type error occurred: {error}. Ensure that the function submitted is callable and that the arguments are of the correct type.",
        "KeyboardInterrupt":"Execution was interrupted by the user. The ongoing tasks may not have completed successfully.",
        "RuntimeError":"The ThreadPoolExecutor has already been shut down and cannot be reused. Please create a new executor instance for further tasks.",
        "ImportError":"Failed to import a required module: {error}. Ensure that all dependencies are correctly installed and accessible."
    }

    ##error text
    error_text = {
        "device_details_error":"!!! You have provided wrong details of the device !!!".center(shutil.get_terminal_size().columns),
        "limit_exceed":"You have reached your limit",
        "Unsuccessful_File_Creation":"Your File Have not been created",
        "wrong_value":"You have provided the wrong value",
        "menu_wrong_input":"Your given input is not presented in the menu",
        "Unvalid_ip_address":"Your IP Address is not valid",
        "Device invalid":"Device is not reachable",
        "Connectivity_Issue":"Please Check your internet connection or device reachability",
        "callable_error":"Class does not have a `__call__` method",
        "Failed_File_Creation":"Failed to create the file process"
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