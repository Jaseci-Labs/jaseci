from __future__ import annotations
from jaclang import *


class Adder(Walker):
    @with_entry
    @Jac.impl_patch_filename("data_spatial_spawn_expressions.jac")
    def do(self, here: Root) -> None:
        here.connect(node_a())
        self.visit(here.refs())


class node_a(Node):
    x: int = field(0)
    y: int = field(0)

    @with_entry
    @Jac.impl_patch_filename("data_spatial_spawn_expressions.jac")
    def add(self, here: Adder) -> None:
        self.x = 550
        self.y = 450
        print(int(self.x) + int(self.y))


Adder().spawn(root)
