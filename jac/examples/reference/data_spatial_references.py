from __future__ import annotations
from jaclang import *


@walker
class Creator:

    @with_entry
    def create(self, here: Jac.RootType) -> None:
        end = here
        i = 0
        while i < 3:
            Jac.connect(end, (end := node_a(val=i)))
            i += 1

        Jac.connect(
            end,
            (end := node_a(val=i + 10)),
            edge=connector,
            conn_assign=(("value",), (i,)),
        )
        Jac.connect(
            (end := node_a(val=i + 10)),
            root(),
            edge=connector,
            conn_assign=(("value",), (i,)),
        )
        Jac.visit(self, Jac.refs(here))


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


Jac.spawn(root(), Creator())
