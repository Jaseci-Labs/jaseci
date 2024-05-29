from __future__ import annotations
from jaclang.plugin.feature import JacFeature as Jac
from dataclasses import dataclass


@Jac.make_walker(on_entry=[Jac.DSFunc("func2", Jac.get_root_type())], on_exit=[])
@dataclass(eq=False)
class Creator:

    def func2(self, here: Jac.get_root_type()) -> None:
        end = here
        i = 0
        while i < 5:
            Jac.connect(
                end, (end := node_1(val=i + 1)), Jac.build_edge(False, None, None)
            )
            i += 1
        if Jac.visit_node(
            self,
            Jac.edge_ref(here, None, Jac.EdgeDir.OUT, filter_func=None),
        ):
            pass


@Jac.make_node(on_entry=[Jac.DSFunc("func_1", Creator)], on_exit=[])
@dataclass(eq=False)
class node_1:
    val: int

    def func_1(self, here: Creator) -> None:
        print("visiting ", self)
        if Jac.visit_node(
            here,
            Jac.edge_ref(self, None, Jac.EdgeDir.OUT, filter_func=None),
        ):
            pass


Jac.spawn_call(Jac.get_root(), Creator())
Jac.spawn_call(Jac.get_root(), Creator())
