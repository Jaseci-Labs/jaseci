from __future__ import annotations
from jaclang import *


def print_base_classes(cls: type) -> type:
    print(
        f"Base classes of {cls.__name__}: {JacList([c.__name__ for c in cls.__bases__])}"
    )
    return cls


class Animal:
    pass


class Domesticated(Obj):
    pass


@print_base_classes
class Pet(Animal, Domesticated, Node):
    pass


class Person(Animal, Walker):
    pass


class Feeder(Person, Walker):
    pass


@print_base_classes
class Zoologist(Feeder, Walker):
    pass
