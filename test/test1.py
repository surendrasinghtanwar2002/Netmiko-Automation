
from netmiko import ConnectHandler

# Step 3: Connect to the Device and Apply Configuration
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.120',
    'username': 'admin',
    'password': 'hackerzone',
}

try:
    # Establish a connection to the network device
    connection = ConnectHandler(**device)
    
    output  = connection.send_command("show vlan brief")
    print(output)
    
    # Disconnect from the device after configuration
    connection.disconnect()
    print("Configuration applied successfully.")

except Exception as e:
    print(f"Error occurred: {e}")


all_output+= f"Your All Commands Output".center(shutil.get_terminal_size().columns) +"\n" +output