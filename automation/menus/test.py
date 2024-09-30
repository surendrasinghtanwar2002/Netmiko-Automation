# Sample list of dictionaries
device_list = [
    {"hostname": "Switch1", "ip_address": "192.168.1.1", "model": "Cisco"},
    {"hostname": "Router1", "ip_address": "192.168.1.2", "model": "Juniper"},
    {"hostname": "Switch2", "ip_address": "192.168.1.3", "model": "HP"},
    {"hostname": "Firewall1", "ip_address": "10.0.0.1", "model": "Fortinet"}
]

filter_ip = ["192.168.1.1","192.168.1.2","192.168.1.3"]


valid_host = []

for items in device_list:
    for valid_ip in filter_ip:
        if items["ip_address"] == valid_ip:
            valid_host.append(items)
        else:
            print("items not found")

# if __name__ == "__main__":
print(valid_host)
