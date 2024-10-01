import re

# Example multiline string
text = """Proceed with reload? [confirm]
This is a test line.
Another line without prompts.
Enter username: [confirm]
Final line?"""

# Regex pattern to match lines with [confirm] or ?
pattern = r'^(.*?\[confirm\].*?|.*?\?.*?)$'

# Find all matching lines
matches = re.findall(pattern, text, re.MULTILINE)

# Print the matching lines for user input
for match in matches:
    print(match.strip())