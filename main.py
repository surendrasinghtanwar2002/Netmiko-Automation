from automation.depen_container.depen_container import DIContainer

def main()->None:
    container = DIContainer()
    main_menu = container.get_main_menu()
    main_menu.display()                 ##Main Display Function

if __name__ == "__main__":
    main()
