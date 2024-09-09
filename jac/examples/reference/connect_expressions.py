from __future__ import annotations
from jaclang.plugin.feature import JacFeature as Jac
from dataclasses import dataclass


@Jac.make_node(on_entry=[], on_exit=[])
@dataclass(eq=False)
class node_a:
    value: int


@Jac.make_walker(
    on_entry=[
        Jac.DSFunc("create", Jac.get_root_type()),
        Jac.DSFunc("travel", Jac.get_root_type() | node_a),
    ],
    on_exit=[],
)
@dataclass(eq=False)
class Creator:

    def create(self, here: Jac.get_root_type()) -> None:
        end = here
        i = 0
        while i < 7:
            if i % 2 == 0:
                Jac.connect(
                    end, (end := node_a(value=i)), Jac.build_edge(False, None, None)
                )
            else:
                Jac.connect(
                    end,
                    (end := node_a(value=i + 10)),
                    Jac.build_edge(False, MyEdge, (("val",), (i,))),
                )
            i += 1

    def travel(self, here: Jac.get_root_type() | node_a) -> None:
        for i in Jac.edge_ref(
            here,
            None,
            Jac.EdgeDir.OUT,
            filter_func=lambda x: [i for i in x if isinstance(i, MyEdge) if i.val <= 6],
        ):
            print(i.value)
        if Jac.visit_node(
            self,
            Jac.edge_ref(here, None, Jac.EdgeDir.OUT, filter_func=None),
        ):
            pass


@Jac.make_edge(on_entry=[], on_exit=[])
@dataclass(eq=False)
class MyEdge:
    val: int = Jac.has_instance_default(gen_func=lambda: 5)


Jac.spawn_call(Jac.get_root(), Creator())
