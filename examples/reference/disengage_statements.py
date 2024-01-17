from __future__ import annotations
from jaclang.plugin.feature import JacFeature as jac


@jac.make_architype("walker", on_entry=[jac.DSFunc("func2", jac.RootType)], on_exit=[])
class walker_1:
    def func2(self, walker_node: jac.RootType) -> None:
        end = walker_node
        i = 0
        while i < 5:
            jac.connect(
                end,
                (end := node_1(val=i + 1)),
                jac.build_edge(jac.EdgeDir.OUT, None, None),
            )
            i += 1
        if jac.visit_node(self, jac.edge_ref(walker_node, jac.EdgeDir.OUT, None)):
            pass


@jac.make_architype("node", on_entry=[jac.DSFunc("func_1", walker_1)], on_exit=[])
class node_1:
    val: int

    def func_1(self, node_here: walker_1) -> None:
        print("visiting ", self)
        if self.val == 3:
            print("Disengaging traversal in node with value 3.")
            jac.disengage(node_here)
            return
        if jac.visit_node(node_here, jac.edge_ref(self, jac.EdgeDir.OUT, None)):
            pass
        else:
            print("finished visitng all nodes  ....\n")


@jac.make_architype("node", on_entry=[], on_exit=[])
class node2:
    val2: int


jac.spawn_call(jac.get_root(), walker_1())
