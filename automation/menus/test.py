# Sample list of dictionaries
device_list = [
    {"hostname": "Switch1", "ip_address": "192.168.1.1", "model": "Cisco"},
    {"hostname": "Router1", "ip_address": "192.168.1.2", "model": "Juniper"},
    {"hostname": "Switch2", "ip_address": "192.168.1.3", "model": "HP"},
    {"hostname": "Firewall1", "ip_address": "10.0.0.1", "model": "Fortinet"}
]

# Filter function to retrieve IP addresses
def filter_ip(device):
    return "ip_address" in device

# Use filter() to get only those devices that have the key 'ip_address'
filtered_devices = filter(filter_ip, device_list)

# Extracting IP addresses and their values
ip_addresses = [(device["ip_address"], device) for device in filtered_devices]

# Output the results
for ip, device in ip_addresses:
    print(f"IP Address: {ip}")