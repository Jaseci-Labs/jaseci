# Function with decorators, access_modifiers
class Calculator:
    """Calculator object with static method"""

    # static function
    @staticmethod
    def multiply(a, b):
        return a * b


print(Calculator.multiply(9, -2))


# Animal Archetype with an abstract ability
class Animal:
    """Abstract class for making a sound."""

    def make_sound(self):
        raise NotImplementedError("Abstract method 'make_sound' must be overridden")


# Concrete class representing a Dog
class Dog(Animal):
    def make_sound(self):
        return "Woof! Woof!"


# Concrete class representing a Cat
class Cat(Animal):
    def make_sound(self):
        return "Meow!"


# Ability to simulate interactions with animals
def interact_with_animal(animal):
    sound = animal.make_sound()
    print(f"The animal says: {sound}")


# Creating instances of concrete archetypes
Milo = Dog()
Leo = Cat()

# Interacting with animals
interact_with_animal(Milo)
interact_with_animal(Leo)


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
