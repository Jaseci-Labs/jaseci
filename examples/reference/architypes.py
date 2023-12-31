# Defining the base class
class Animal:
    def __init__(self):
        self.type = "Animal"


# Defining another base class
class Domesticated:
    def __init__(self):
        self.domesticated = True


# Defining the first derived class with multiple inheritance
class Mammal(Animal, Domesticated):
    def __init__(self):
        Animal.__init__(self)
        Domesticated.__init__(self)
        self.classification = "Mammal"


# Defining the second derived class
class Dog(Mammal):
    def __init__(self):
        super().__init__()
        self.species = "Dog"


# Defining the third derived class
class Labrador(Dog):
    def __init__(self):
        super().__init__()
        self.breed = "Labrador"


def print_hierarchy(cls):
    """
    Recursively collects all base classes in the inheritance hierarchy of the given class.
    """
    bases = list(cls.__bases__)
    for base in bases:
        bases.extend(print_hierarchy(base))
    return bases


def print_base_classes(cls):
    """
    Decorator that prints all classes in the inheritance hierarchy of the given class.
    """

    def wrapper():
        hierarchy = print_hierarchy(cls)
        unique_hierarchy = set(h.__name__ for h in hierarchy)  # Remove duplicates
        print(
            f"Classes in the hierarchy of {cls.__name__}: {', '.join(unique_hierarchy)}"
        )
        return cls()

    return wrapper


# Applying the decorator to the last class
@print_base_classes
class DecoratedLabrador(Labrador):
    pass


# Example of using the decorated class
decorated_labrador = (
    DecoratedLabrador()
)  # This prints the base classes of DecoratedLabrador
