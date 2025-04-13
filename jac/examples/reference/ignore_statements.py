from __future__ import annotations
from jaclang import *


@walker
class Visitor:
    @with_entry
    def travel(self, here: Jac.RootType) -> None:
        Jac.ignore(self, Jac.refs(here)[0])
        if not Jac.visit(self, Jac.refs(here)):
            Jac.visit(self, root())


@node
class item:
    @with_entry
    def speak(self, here: Visitor) -> None:
        print("Hey There!!!")


i = 0
while i < 5:
    Jac.connect(root(), item())
    i += 1

Jac.spawn(root(), Visitor())
