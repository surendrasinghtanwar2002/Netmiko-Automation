import shutil

class Text_File:
    def __init__(self) -> None:
        pass

    ##common text
    common_text ={
        "connection": "Connected to the host succesfully",
        "connected_host":"Connected to host ",
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
        "proceed_confirmation":"Do you want to proceed (Yes/No):-",
        "Data_retrieved":"Succesfully Data have been retrieved",
        "Successful_File_Creation":"Your File Have been created Succesfully",
        "File_save_permission":"Do you wan,t to say to your file (Yes/No)",
        "Json_conversion_permission":"Do you want to convert raw data into json",
        "Exit_Permission":"Do you wan't to exit from the menu"
    }
    ##common text
    exception_text ={
        "common_function_exception": "Your function have exception",
        "value_error":"You have passed wrong value",
        "CalledProcessError":"Subprocess Exception occured",
        "file_not_found":"File not Founded Exception"

    }
    ##error text
    error_text = {
        "device_details_error":"!!! You have provided wrong details of the device !!!".center(shutil.get_terminal_size().columns),
        "limit_exceed":"You have reached your limit",
        "Unsuccessful_File_Creation":"Your File Have not been created"
    }
    ##debug text
    debug_text = {
        "device_details": "We got the device details",
        "device_respond":"Device is Active".center(shutil.get_terminal_size().columns),
    }