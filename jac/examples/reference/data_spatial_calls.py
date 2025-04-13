from __future__ import annotations
from jaclang import *


@walker
class Creator:

    @with_entry
    def func2(self, here: Jac.RootType) -> None:
        end = here
        i = 0
        while i < 5:
            Jac.connect(end, (end := node_1(val=i + 1)))
            i += 1
        Jac.visit(self, Jac.refs(here))


@node
class node_1:
    val: int

    @with_entry
    def func_1(self, here: Creator) -> None:
        print("visiting ", self)
        Jac.visit(here, Jac.refs(self))


Jac.spawn(root(), Creator())
Jac.spawn(root(), Creator())
