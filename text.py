# import re
import time
# # Example multiline string
# text = """Proceed with reload? [confirm]
# This is a test line.
# Another line without prompts.
# Enter username: [confirm]
# Final line?"""

# # Regex pattern to match lines with [confirm] or ?
# pattern = r'^(.*?\[confirm\].*?|.*?\?.*?)$'

# # Find all matching lines
# matches = re.findall(pattern, text, re.MULTILINE)

# # Print the matching lines for user input
# for match in matches:
#     print(match.strip())

def write_backup_configuration():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    final_final_name = f"Today Backup {timestr}"
    with open(final_final_name,"w") as file:
        if file.write("hello world my name is surendra"):
            print("Yes file have been created")
        else:
            print("File is not creatd")

if __name__ == "__main__":
    write_backup_configuration()