from __future__ import annotations
from jaclang.plugin.feature import JacFeature as jac


@jac.make_architype("walker", on_entry=[jac.DSFunc("func2", jac.RootType)], on_exit=[])
class Creator:
    def func2(self, creator_here: jac.RootType) -> None:
        end = creator_here
        i = 0
        while i < 5:
            jac.connect(
                end,
                (end := node_1(val=i + 1)),
                jac.build_edge(jac.EdgeDir.OUT, None, None),
            )
            i += 1
        if jac.visit_node(
            self, jac.edge_ref(creator_here, jac.EdgeDir.OUT, None, None)
        ):
            pass


@jac.make_architype("node", on_entry=[jac.DSFunc("func_1", Creator)], on_exit=[])
class node_1:
    val: int

    def func_1(self, node_here: Creator) -> None:
        print("visiting ", self)
        if jac.visit_node(node_here, jac.edge_ref(self, jac.EdgeDir.OUT, None, None)):
            pass


jac.spawn_call(jac.get_root(), Creator())
jac.spawn_call(jac.get_root(), Creator())
