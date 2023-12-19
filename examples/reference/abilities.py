# Function with decorators, access_modifiers
class Calculator:
    """Calculator object with static method"""

    # static function
    @staticmethod
    def multiply(a, b):
        return a * b


print(Calculator.multiply(9, -2))


# Declaration & Definition in same block
def greet(name):
    print(f"Hey, {name} Welcome to Jaseci!")


# fun calling
greet("Coder")


# Simple Function
def add(*a):
    """Ability(Function) to calculate the numbers"""
    return sum(a)


# function calling
print(add(9, -3, 4))
