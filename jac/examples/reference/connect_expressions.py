from __future__ import annotations
from jaclang.plugin.feature import JacFeature as Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass


@Jac.make_node(on_entry=[], on_exit=[])
@dataclass(eq=False)
class node_a(Jac.Node):
    value: int


@Jac.make_walker(on_entry=[Jac.DSFunc("create"), Jac.DSFunc("travel")], on_exit=[])
@dataclass(eq=False)
class Creator(Jac.Walker):
    def create(self, _jac_here_: Jac.RootType) -> None:
        end = _jac_here_
        i = 0
        while i < 7:
            if i % 2 == 0:
                Jac.connect(
                    left=end,
                    right=(end := node_a(value=i)),
                    edge_spec=Jac.build_edge(
                        is_undirected=False, conn_type=None, conn_assign=None
                    ),
                )
            else:
                Jac.connect(
                    left=end,
                    right=(end := node_a(value=i + 10)),
                    edge_spec=Jac.build_edge(
                        is_undirected=False,
                        conn_type=MyEdge,
                        conn_assign=(("val",), (i,)),
                    ),
                )
            i += 1

    def travel(self, _jac_here_: Jac.RootType | node_a) -> None:
        for i in Jac.edge_ref(
            _jac_here_,
            target_obj=None,
            dir=Jac.EdgeDir.OUT,
            filter_func=lambda x: [i for i in x if isinstance(i, MyEdge) if i.val <= 6],
            edges_only=False,
        ):
            print(i.value)
        if Jac.visit_node(
            self,
            Jac.edge_ref(
                _jac_here_,
                target_obj=None,
                dir=Jac.EdgeDir.OUT,
                filter_func=None,
                edges_only=False,
            ),
        ):
            pass


@Jac.make_edge(on_entry=[], on_exit=[])
@dataclass(eq=False)
class MyEdge(Jac.Edge):
    val: int = Jac.has_instance_default(gen_func=lambda: 5)


if __name__ == "__main__":
    Jac.spawn_call(Jac.get_root(), Creator())
