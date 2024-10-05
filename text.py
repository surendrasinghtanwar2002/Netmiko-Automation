class A:
    def __init__(self, value):
        self.value = value

    def display_value(self):
        print(f"Value from class A: {self.value}")

class B(A):
    def passing_values(self, values):
        # Loop through a list of values and pass them to class A using super()
        for value in values:
            super().__init__(value)  # Call class A's constructor with each value
            self.display_value()     # Display the value from class A

# Example usage:
b = B(0)  # Initial value can be passed here but will be overwritten
b.passing_values([10, 20, 30])  # Pass multiple values in a list