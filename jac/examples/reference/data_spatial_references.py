from __future__ import annotations
from jaclang import *


@walker
class Creator:

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
            root(), edge=connector, conn_assign=(("value",), (i,))
        )
        self.visit(here.refs())


@node
class node_a:
    val: int

    @with_entry
    def make_something(self, here: Creator) -> None:
        i = 0
        while i < 5:
            print(f"wlecome to {self}")
            i += 1


@edge
class connector:
    value: int = field(10)


root().spawn(Creator())
