from jaclang.plugin.feature import JacFeature as Jac


def print_base_classes(cls: type) -> type:
    print(f"Base classes of {cls.__name__}: {[c.__name__ for c in cls.__bases__]}")
    return cls


class Animal:
    pass


class Domesticated:
    pass


@print_base_classes
@Jac.make_architype("node", on_entry=[], on_exit=[])
class Mammal(Animal, Domesticated):
    pass


@Jac.make_architype("walker", on_entry=[], on_exit=[])
class Dog(Mammal):
    pass


@Jac.make_architype("walker", on_entry=[], on_exit=[])
class Labrador(Dog):
    pass


@print_base_classes
@Jac.make_architype("walker", on_entry=[], on_exit=[])
class DecoratedLabrador(Labrador):
    pass
