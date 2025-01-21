from __future__ import annotations
from jaclang import *


def print_base_classes(cls: type) -> type:
    print(
        f"Base classes of {cls.__name__}: {List([c.__name__ for c in cls.__bases__])}"
    )
    return cls


class Animal(Obj):
    pass


class Domesticated(Obj):
    pass


@print_base_classes
class Pet(Animal, Domesticated, Obj):
    pass


class Person(Animal, Obj):
    pass


class Feeder(Person, Obj):
    pass


@print_base_classes
class Zoologist(Feeder, Obj):
    pass
