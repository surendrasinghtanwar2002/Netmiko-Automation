from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler

class MultipleDeviceConnection:
    def __init__(self, device_details: list) -> None:
        self.device_details = device_details
        self.commands_list = [
            ["show ip interface brief", "show running-config", "show calendar", "write"],
            ["show ip interface brief", "show running-config", "show calendar", "write"]
        ]
        self.command_results = ""

    def netmiko_connection(self, device):
        try:
            with ConnectHandler(**device) as connection:
                print(f"Connected to {device['host']}")
                # Send commands immediately after connecting
                result = self.command_send(connection, self.commands_list[0])
                self.command_results += f"Results from {device['host']}:\n{result}\n"
        except Exception as e:
            print(f"Failed to connect to {device['host']}: {e}")
            self.command_results += f"Failed to connect to {device['host']}: {e}\n"

    def command_send(self, connection, commands):
        results = ""
        for command in commands:
            try:
                result = connection.send_command(command, use_textfsm=True)
                results += f"{command}:\n{result}\n"
            except Exception as e:
                results += f"Command '{command}' failed: {e}\n"
        return results

    def threading_module(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.netmiko_connection, self.device_details)

        return self.command_results

if __name__ == "__main__":
    devices = [
        {"device_type": "cisco_ios", "host": "192.168.1.100", "username": "admin", "password": "hackerzone"},
        {"device_type": "cisco_ios", "host": "192.168.1.105", "username": "admin", "password": "hackerzone"},
        {"device_type": "cisco_ios", "host": "192.168.1.110", "username": "admin", "password": "hackerzone"},
        {"device_type": "cisco_ios", "host": "192.168.1.115", "username": "admin", "password": "hackerzone"},
    ]
    
    t1 = MultipleDeviceConnection(device_details=devices)
    result = t1.threading_module()
    print(result)
