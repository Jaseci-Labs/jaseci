from __future__ import annotations
from jaclang.plugin.feature import JacFeature as Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass


@Jac.make_walker(on_entry=[Jac.DSFunc("travel")], on_exit=[])
@dataclass(eq=False)
class Visitor(Jac.Walker):

    def travel(self, _jac_here_: Jac.RootType) -> None:
        Jac.ignore(
            self,
            Jac.edge_ref(
                _jac_here_,
                target_obj=None,
                dir=Jac.EdgeDir.OUT,
                filter_func=None,
                edges_only=False,
            )[0],
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
        elif Jac.visit_node(self, Jac.get_root()):
            pass


@Jac.make_node(on_entry=[Jac.DSFunc("speak")], on_exit=[])
@dataclass(eq=False)
class item(Jac.Node):

    def speak(self, _jac_here_: Visitor) -> None:
        print("Hey There!!!")


i = 0
while i < 5:
    Jac.connect(
        left=Jac.get_root(),
        right=item(),
        edge_spec=Jac.build_edge(is_undirected=False, conn_type=None, conn_assign=None),
    )
    i += 1
Jac.spawn_call(Jac.get_root(), Visitor())
