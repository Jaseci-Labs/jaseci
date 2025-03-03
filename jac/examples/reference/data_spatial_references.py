from __future__ import annotations
from jaclang import *


class Creator(Walker):

    @with_entry
    def create(self, here: Root) -> None:
        end = here
        i = 0
        while i < 3:
            end.connect((end := node_a(val=i)))
            i += 1
        end.connect(
            (end := node_a(val=i + 10)), edge=connector, conn_assign=(("value",), (i,))
        )
        (end := node_a(val=i + 10)).connect(
            root, edge=connector, conn_assign=(("value",), (i,))
        )
        self.visit(here.refs())


class node_a(Node):
    val: int

    @with_entry
    def make_something(self, here: Creator) -> None:
        i = 0
        while i < 5:
            print(f"wlecome to {self}")
            i += 1


class connector(Edge):
    value: int = field(10)


root.spawn(Creator())
