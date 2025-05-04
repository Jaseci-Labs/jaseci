"""Test file for type binding functionality."""


# Define a simple class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name}"

    def birthday(self):
        self.age += 1


# Define a function
def add(a, b):
    return a + b


# Main function
def main():
    # Variables
    x = 5
    y = 3.14
    s = "Hello, world!"
    b = True

    # Function call
    result = add(10, 20)

    # Class instantiation
    person = Person("Alice", 30)
    greeting = person.greet()
    person.birthday()

    return "All tests completed"


if __name__ == "__main__":
    main()
