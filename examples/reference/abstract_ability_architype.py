from abc import ABC, abstractmethod

# Animal abstaract class with an abstract methods
class Animal(ABC):
    """Abstract class for animals."""

    @abstractmethod
    def make_sound(self):
        """Abstract method for making a sound."""
        pass

# Concrete class representing a Dog
class Dog(Animal):
    """Class representing a Dog."""

    def make_sound(self):
        """Method to make a dog sound."""
        return "Woof! Woof!"

# Concrete class representing a Cat
class Cat(Animal):
    """Class representing a Cat."""

    def make_sound(self):
        """Method to make a cat sound."""
        return "Meow!"

# Function to simulate interactions with animals
def interact_with_animal(animal: Animal):
    """Function to interact with an animal and make it sound."""
    sound = animal.make_sound()
    print(f"The animal says: {sound}")


# Creating instances of concrete classes
Milo = Dog()
Leo = Cat()

# Interacting with animals
interact_with_animal(Milo)
interact_with_animal(Leo)
