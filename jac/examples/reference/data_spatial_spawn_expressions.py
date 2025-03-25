from __future__ import annotations
from jaclang import *


@walker
class Adder:
    @with_entry
    def do(self, here: Root) -> None:
        here.connect(node_a())
        self.visit(here.refs())


@node
class node_a:
    x: int = field(0)
    y: int = field(0)

    @with_entry
    def add(self, here: Adder) -> None:
        self.x = 550
        self.y = 450
        print(int(self.x) + int(self.y))


Adder().spawn(root())
