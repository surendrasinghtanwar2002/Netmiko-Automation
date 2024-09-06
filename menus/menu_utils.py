
##display menu function
def display_menu(menu_items):
    try:
        from clearscreen import clear
        clear()  # Define clear() function in display.py
        for index, item in enumerate(menu_items, start=1):
            print(f"({index}) {item}")
    except ValueError as valueerror:
        print("Value error:", valueerror)
    except Exception as error:
        print("An error occurred:", error)

##get user_choice_details
def get_user_choice(menu_actions):
    try:
        while True:
            choice = input("Enter your choice: ")
            if choice in menu_actions:
                return choice
            print(f"Invalid choice. Please enter a number between 1 and {len(menu_actions)}.")
    except ValueError as valuerror:
        print("Value error:", valuerror)
    except Exception as error:
        print("An error occurred:", error)