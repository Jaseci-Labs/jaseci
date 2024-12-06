from __future__ import annotations
from jaclang.plugin.feature import JacFeature as Jac
from dataclasses import dataclass as dataclass


# Since the Jac class cannot be inherit from object, (cause the base class will be changed at run time)
# we need a base class.
#
# reference: https://stackoverflow.com/a/9639512/10846399
#
class Base:
    pass


@Jac.make_obj(on_entry=[], on_exit=[])
@dataclass(eq=False)
class Point(Base):
    x: float
    y: float


data = Point(x=9, y=0)
match data:
    case Point(int(a), y=0):
        print(f"Point with x={a} and y=0")
    case _:
        print("Not on the x-axis")
