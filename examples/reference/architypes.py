from jaclang.plugin.feature import JacFeature as jac


def print_base_classes(cls: type) -> type:
    print(f"Base classes of {cls.__name__}: {[c.__name__ for c in cls.__bases__]}")
    return cls


@jac.make_obj(on_entry=[], on_exit=[])
class Animal(jac.Obj):
    pass


@jac.make_obj(on_entry=[], on_exit=[])
class Domesticated(jac.Obj):
    pass


@print_base_classes
@jac.make_node(on_entry=[], on_exit=[])
class Mammal(Animal, Domesticated, jac.Node):
    pass


@jac.make_walker(on_entry=[], on_exit=[])
class Dog(Mammal, jac.Walker):
    pass


@jac.make_walker(on_entry=[], on_exit=[])
class Labrador(Dog, jac.Walker):
    pass


@print_base_classes
@jac.make_walker(on_entry=[], on_exit=[])
class DecoratedLabrador(Labrador, jac.Walker):
    pass
