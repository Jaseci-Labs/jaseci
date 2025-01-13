from jaclang.plugin.feature import JacFeature as jac


def print_base_classes(cls: type) -> type:
    print(f"Base classes of {cls.__name__}: {[c.__name__ for c in cls.__bases__]}")
    return cls


# Since the Animal class cannot be inherit from object, (cause the base class will be changed at run time)
# we need a base class.
#
# reference: https://stackoverflow.com/a/9639512/10846399
#
class Base:
    pass


@jac.make_obj(on_entry=[], on_exit=[])
class Animal(Base):
    pass


@jac.make_obj(on_entry=[], on_exit=[])
class Domesticated(jac.Obj):
    pass


@print_base_classes
@jac.make_node(on_entry=[], on_exit=[])
class Pet(Animal, Domesticated, jac.Node):
    pass


@jac.make_walker(on_entry=[], on_exit=[])
class Person(Animal, jac.Walker):
    pass


@jac.make_walker(on_entry=[], on_exit=[])
class Feeder(Person, jac.Walker):
    pass


@print_base_classes
@jac.make_walker(on_entry=[], on_exit=[])
class Zoologist(Feeder, jac.Walker):
    pass
