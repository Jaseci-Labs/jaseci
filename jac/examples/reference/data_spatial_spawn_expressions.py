from __future__ import annotations
from jaclang import *


@walker
class Adder:
    @with_entry
    def do(self, here: Jac.RootType) -> None:
        Jac.connect(here, node_a())
        Jac.visit(self, Jac.refs(here))


@node
class node_a:
    x: int = field(0)
    y: int = field(0)

    @with_entry
    def add(self, here: Adder) -> None:
        self.x = 550
        self.y = 450
        print(int(self.x) + int(self.y))


Jac.spawn(Adder(), root())
