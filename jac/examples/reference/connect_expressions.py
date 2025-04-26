from __future__ import annotations
from jaclang.runtimelib.builtin import *
from jaclang import JacMachine as _


class node_a(_.Node):
    value: int


class Creator(_.Walker):

    @_.entry
    @_.impl_patch_filename(
        "/home/boyong/jaseci/jac/examples/reference/connect_expressions.jac"
    )
    def create(self, here: _.Root) -> None:
        end = here
        i = 0
        while i < 7:
            if i % 2 == 0:
                _.connect(end, (end := node_a(value=i)))
            else:
                _.connect(
                    end,
                    (end := node_a(value=i + 10)),
                    edge=MyEdge,
                    conn_assign=(("val",), (i,)),
                )
            i += 1

    @_.entry
    @_.impl_patch_filename(
        "/home/boyong/jaseci/jac/examples/reference/connect_expressions.jac"
    )
    def travel(self, here: _.Root | node_a) -> None:
        for i in _.refs(
            here, filter=lambda item: isinstance(item, MyEdge) and item.val <= 6
        ):
            print(i.value)
        _.visit(self, _.refs(here))


class MyEdge(_.Edge):
    val: int = 5


if __name__ == "__main__":
    _.spawn(_.root(), Creator())
