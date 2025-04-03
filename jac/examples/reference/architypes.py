from __future__ import annotations
from jaclang import *


def print_base_classes(cls: type) -> type:
    print(
        f"Base classes of {cls.__name__}: {JacList([c.__name__ for c in cls.__bases__])}"
    )
    return cls


class Animal:
    pass


@obj
class Domesticated:
    pass


@node
@print_base_classes
class Pet(Animal, Domesticated):
    pass


@walker
class Person(Animal):
    pass


@walker
class Feeder(Person):
    pass


@walker
@print_base_classes
class Zoologist(Feeder):
    pass
