class Parent:
    def __init__(self, data):
        self.data = "harish parmater"

class Child(Parent):
    def display_data(self):
        print(self.data)

# Example usage
if __name__ == "__main__":
    # Create an instance of Child
    child_instance = Child()
    print(child_instance.data)