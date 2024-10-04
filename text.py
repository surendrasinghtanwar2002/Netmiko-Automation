class A:
    def __init__(self, command):
        self.command = command
    
    def checkingcondition(self):
        return(f"We have printed hello {self.command}")

class B(A):
    def __init__(self,):
        pass

    def calling_parentclass(self):
        for items in range(20):
            super().__init__(items)
            print(self.checkingcondition())
    

# Create an instance of class B, passing arguments for A's attributes
t1 = B()
t1.calling_parentclass()