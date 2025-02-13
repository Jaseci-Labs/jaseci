from __future__ import annotations
from jaclang.plugin.feature import JacFeature as Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass


@Jac.make_walker(on_entry=[Jac.DSFunc("create")], on_exit=[])
@dataclass(eq=False)
class Creator(Jac.Walker):
    def create(self, _jac_here_: Jac.Root) -> None:
        end = _jac_here_
        i = 0
        while i < 3:
            Jac.connect(
                left=end,
                right=(end := node_a(val=i)),
                edge_spec=Jac.build_edge(
                    is_undirected=False, conn_type=None, conn_assign=None
                ),
            )
            i += 1
        Jac.connect(
            left=end,
            right=(end := node_a(val=i + 10)),
            edge_spec=Jac.build_edge(
                is_undirected=False, conn_type=connector, conn_assign=(("value",), (i,))
            ),
        )
        Jac.connect(
            left=(end := node_a(val=i + 10)),
            right=Jac.get_root(),
            edge_spec=Jac.build_edge(
                is_undirected=False, conn_type=connector, conn_assign=(("value",), (i,))
            ),
        )
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


@Jac.make_node(on_entry=[Jac.DSFunc("make_something")], on_exit=[])
@dataclass(eq=False)
class node_a(Jac.Node):
    val: int

    def make_something(self, _jac_here_: Creator) -> None:
        i = 0
        while i < 5:
            print(f"wlecome to {self}")
            i += 1


@Jac.make_edge(on_entry=[], on_exit=[])
@dataclass(eq=False)
class connector(Jac.Edge):
    value: int = Jac.has_instance_default(gen_func=lambda: 10)


Jac.spawn_call(Jac.get_root(), Creator())
