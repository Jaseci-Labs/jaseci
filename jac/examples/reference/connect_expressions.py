from __future__ import annotations
from jaclang import *

class node_a(Node):
    value: int

class Creator(Walker):
    @with_entry
    @Jac.impl_patch_filename('connect_expressions.jac')
    def create(self, here: Root) -> None:
        end = here
        i = 0
        while i < 7:
            if i % 2 == 0:
                end.connect((end := node_a(value=i)))
            else:
                end.connect((end := node_a(value=i + 10)), edge=MyEdge, conn_assign=(('val',), (i,)))
            i += 1

    @with_entry
    @Jac.impl_patch_filename('connect_expressions.jac')
    def travel(self, here: Root | node_a) -> None:
        for i in here.refs(MyEdge, lambda edge: edge.val <= 6):
            print(i.value)
        self.visit(here.refs())

class MyEdge(Edge):
    val: int = field(5)

if __name__ == '__main__':
    root.spawn(Creator())
