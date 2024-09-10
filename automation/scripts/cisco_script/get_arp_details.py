import typing
from assets.text_file import Text_File

def get_arp_details(*args, **kwargs) -> typing.Optional[str]:
    try:
        netmiko_connection = args[0]  # Unwrapping the tuple
        result = netmiko_connection.send_command("show arp", strip_prompt=False, strip_command=False)
        if result:
            print(Text_File.common_text["Data_retrieved"])
            return result
        else:
            print(Text_File.error_text)
            return None
        
    except Exception as e:
        print(Text_File.exception_text["common_function_exception"], e)
        return None

# ##Main function calls here 
def main(*args, **kwargs):
    return get_arp_details(*args, **kwargs)

if __name__ == "__main__":
    result = main() 