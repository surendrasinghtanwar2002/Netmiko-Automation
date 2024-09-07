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
        "host_ip_prompt":"Enter your HOST IP ADDRESS",
        "mutli_auth_welcome":" Welcome to Multi Device Connection Authentication Page ".center(shutil.get_terminal_size().columns,"!"),
        "same_credentials":"Do you have same credentaisl for all device (Yes/No):-",
        "range_of_ip":"Specify number of device IP Address Range:-",
        "ip_address_range":"Enter Your Ip Address no"

    }
    ##common text
    exception_text ={
        "common_function_exception": "Your function have exception",
        "value_error":"You have passed wrong value",
    }
    ##error text
    error_text = {
        "device_details_error":"!!! You have provided wrong details of the device !!!".center(shutil.get_terminal_size().columns),
        "limit_exceed":"You have reached your limit"
    }
    ##debug text
    debug_text = {
        "device_details": "We got the device details"
    }