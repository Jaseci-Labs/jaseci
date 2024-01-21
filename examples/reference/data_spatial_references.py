from __future__ import annotations
from jaclang.plugin.feature import JacFeature as jac
import random


@jac.make_architype("node", on_entry=[], on_exit=[])
class MyNode:
    value: int


@jac.make_architype("edge", on_entry=[], on_exit=[])
class MyEdge:
    val: int = 5


@jac.make_architype(
    "walker",
    on_entry=[
        jac.DSFunc("create", jac.RootType),
        jac.DSFunc("do_something", jac.RootType),
    ],
    on_exit=[],
)
class Walk:
    def create(self, walker_here: jac.RootType) -> None:
        i = 0
        while i < 5:
            jac.connect(
                jac.get_root(),
                MyNode(value=i + 1),
                jac.build_edge(
                    jac.EdgeDir.OUT, MyEdge, (("val",), (random.randint(1, 10),))
                ),
            )
            jac.connect(
                walker_here,
                MyNode(value=i + 1),
                jac.build_edge(jac.EdgeDir.OUT, None, None),
            )
            i += 1
        if jac.visit_node(self, jac.edge_ref(walker_here, jac.EdgeDir.OUT, None)):
            pass

    def do_something(self, walker_here: jac.RootType) -> None:
        for i in (lambda x: [i for i in x if i.val <= 5])(
            jac.edge_ref(walker_here, jac.EdgeDir.OUT, MyEdge)
        ):
            print(i.val)
        print("Hello")
        if jac.visit_node(self, jac.edge_ref(walker_here, jac.EdgeDir.OUT, None)):
            pass


jac.spawn_call(jac.get_root(), Walk())
# jac.get_root()._jac_.gen_dot()
