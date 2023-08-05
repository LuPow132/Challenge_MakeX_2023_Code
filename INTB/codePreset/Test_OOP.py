class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."

firstPPL = Person("LuPow",16)
secondPPL = Person("Luana",18)

print(firstPPL.age)
