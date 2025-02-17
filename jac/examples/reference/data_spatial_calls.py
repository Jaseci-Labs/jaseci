from __future__ import annotations
from jaclang.plugin.feature import JacFeature as Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass


@Jac.make_walker(on_entry=[Jac.DSFunc("func2")], on_exit=[])
@dataclass(eq=False)
class Creator(Jac.Walker):
    def func2(self, _jac_here_: Jac.RootType) -> None:
        end = _jac_here_
        i = 0
        while i < 5:
            Jac.connect(
                left=end,
                right=(end := node_1(val=i + 1)),
                edge_spec=Jac.build_edge(
                    is_undirected=False, conn_type=None, conn_assign=None
                ),
            )
            i += 1
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


@Jac.make_node(on_entry=[Jac.DSFunc("func_1")], on_exit=[])
@dataclass(eq=False)
class node_1(Jac.Node):
    val: int

    def func_1(self, _jac_here_: Creator) -> None:
        print("visiting ", self)
        if Jac.visit_node(
            _jac_here_,
            Jac.edge_ref(
                self,
                target_obj=None,
                dir=Jac.EdgeDir.OUT,
                filter_func=None,
                edges_only=False,
            ),
        ):
            pass


Jac.spawn_call(Jac.get_root(), Creator())
Jac.spawn_call(Jac.get_root(), Creator())
