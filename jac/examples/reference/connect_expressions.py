from __future__ import annotations
from jaclang import *


@node
class node_a:
    value: int


@walker
class Creator:
    @with_entry
    def create(self, here: Root) -> None:
        end = here
        i = 0
        while i < 7:
            if i % 2 == 0:
                end.connect((end := node_a(value=i)))
            else:
                end.connect(
                    (end := node_a(value=i + 10)),
                    edge=MyEdge,
                    conn_assign=(("val",), (i,)),
                )
            i += 1

    @with_entry
    def travel(self, here: Root | node_a) -> None:
        for i in here.refs(MyEdge, lambda edge: edge.val <= 6):
            print(i.value)
        self.visit(here.refs())


@edge
class MyEdge:
    val: int = field(5)


if __name__ == "__main__":
    root().spawn(Creator())
