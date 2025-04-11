from __future__ import annotations
from jaclang import *


@node
class node_a:
    value: int


@walker
class Creator:
    @with_entry
    def create(self, here: Jac.RootType) -> None:
        end = here
        i = 0
        while i < 7:
            if i % 2 == 0:
                Jac.conn(end, (end := node_a(value=i)))
            else:
                Jac.conn(
                    end,
                    (end := node_a(value=i + 10)),
                    edge=MyEdge,
                    conn_assign=(("val",), (i,)),
                )
            i += 1

    @with_entry
    def travel(self, here: Jac.RootType | node_a) -> None:
        for i in Jac.refs(here, MyEdge, lambda edge: edge.val <= 6):
            print(i.value)
        Jac.visit(self, Jac.refs(here))


@edge
class MyEdge:
    val: int = field(5)


if __name__ == "__main__":
    Jac.spawn(root(), Creator())
