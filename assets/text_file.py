import shutil

class Text_File:
    def __init__(self) -> None:
        pass

    ##common text
    common_text ={
        "connection": "Connected to the host succesfully",
        "connected_host":"Connected to host "
    }
    ##common text
    exception_text ={
        "common_function_exception": "Your function have exception",
        "value_error":"You have passed wrong value",
    }
    ##error text
    error_text = {
        "device_details_error":"!!! You have provided wrong details of the device !!!".center(shutil.get_terminal_size().columns)
    }
    ##debug text
    debug_text = {
        "device_details": "We got the device details"
    }