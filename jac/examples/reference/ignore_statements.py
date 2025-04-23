from __future__ import annotations
from jaclang.runtimelib.builtin import *
from jaclang import JacFeature as _


class Visitor(_.Walker):

    @_.entry
    def travel(self, here: _.Root) -> None:
        _.ignore(self, _.refs(here)[0])
        if not _.visit(self, _.refs(here)):
            _.visit(self, _.root())


class item(_.Node):

    @_.entry
    def speak(self, here: Visitor) -> None:
        print("Hey There!!!")


i = 0
while i < 5:
    _.connect(_.root(), item())
    i += 1

_.spawn(_.root(), Visitor())
