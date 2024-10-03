# from concurrent.futures import ThreadPoolExecutor
import time

# # Example function to process items from the second list with the current item from the first list
# def process_items(item1, item2):
#     time.sleep(1)  # Simulating a time-consuming task
#     return f'Processed {item1} with {item2}'

# # Main execution function
# def execute_with_control(list1, list2):
#     results = []
    
#     with ThreadPoolExecutor(max_workers=5) as executor:
#         for item1 in list2:
#             # For each item in the first list, submit tasks for all items in the second list
#             futures = [executor.submit(process_items, item1, item2) for item2 in list1]
#             for future in futures:
#                 results.append(future.result())  # Collect results as they complete

#     # Print all results
#     for result in results:
#         print(result)

# # Example usage
# list1 = ["show ip itnerface brief","show running config","show vlan brief"]  # First list
# list2 = ['netmiko_object_1', 'netmiko_object_2', 'netmiko_object_3']  # Second list

# execute_with_control(list1, list2)


# import time
# timestr = time.strftime("%Y%m%d-%H%M%S")
# final_final_name = f"Today Backup {timestr}"
# print(final_final_name)


def write_backup_configuration(self):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    final_final_name = f"Today Backup {timestr}"
    with(final_final_name,"w") as file:
        if file.write("hello world my name is surendra"):
            print("Yes file have been created")
        else:
            print("File is not creatd")
