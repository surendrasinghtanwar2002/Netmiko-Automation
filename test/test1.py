def greet():
    return "Hello!"

def farewell():
    return "Goodbye!"

# Function to call another function dynamically
def call_function(func_name):
    func = getattr(globals(), func_name, None)
    
    if callable(func):
        return func()
    else:
        return f"Function '{func_name}' not found or not callable."

# Dynamically call functions
print(call_function("greet"))    # Output: Hello!
print(call_function("farewell")) # Output: Goodbye!
print(call_function("unknown"))  # Output: Function 'unknown' not found or not callable.
