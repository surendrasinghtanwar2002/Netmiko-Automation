import sys # In some cases, you may need to import the sys module

print("Please close the session".center(120))
user_choice = input("Enter your choice (Yes/No):-").strip().lower()
if user_choice == "yes":
    sys.exit()
else:
    print("We are not exiting the menu")