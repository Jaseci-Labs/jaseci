from __future__ import annotations
from jaclang.plugin.feature import JacFeature as Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass


@Jac.make_walker(on_entry=[Jac.DSFunc("do")], on_exit=[])
@dataclass(eq=False)
class Adder(Jac.Walker):
    def do(self, _jac_here_: Jac.Root) -> None:
        Jac.connect(
            left=_jac_here_,
            right=node_a(),
            edge_spec=Jac.build_edge(
                is_undirected=False, conn_type=None, conn_assign=None
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


@Jac.make_node(on_entry=[Jac.DSFunc("add")], on_exit=[])
@dataclass(eq=False)
class node_a(Jac.Node):
    x: int = Jac.has_instance_default(gen_func=lambda: 0)
    y: int = Jac.has_instance_default(gen_func=lambda: 0)

    def add(self, _jac_here_: Adder) -> None:
        self.x = 550
        self.y = 450
        print(int(self.x) + int(self.y))


Jac.spawn_call(Adder(), Jac.get_root())
