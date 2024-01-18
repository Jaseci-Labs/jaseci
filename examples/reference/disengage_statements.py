from __future__ import annotations
from jaclang.plugin.feature import JacFeature as _Jac


@_Jac.make_architype(
    "walker", on_entry=[_Jac.DSFunc("func2", _Jac.RootType)], on_exit=[]
)
class walker_1:
    def func2(self, _jac_here_: _Jac.RootType) -> None:
        end = _jac_here_
        i = 0
        while i < 5:
            _Jac.connect(
                end,
                (end := node_1(val=i + 1)),
                _Jac.build_edge(_Jac.EdgeDir.OUT, None, None),
            )
            i += 1
        if _Jac.visit_node(self, _Jac.edge_ref(_jac_here_, _Jac.EdgeDir.OUT, None)):
            pass


@_Jac.make_architype("node", on_entry=[_Jac.DSFunc("func_1", walker_1)], on_exit=[])
class node_1:
    val: int

    def func_1(self, _jac_here_: walker_1) -> None:
        print("visiting ", self)
        if self.val == 3:
            print("Disengaging traversal in node with value 3.")
            _Jac.disengage(_jac_here_)
            return
        if _Jac.visit_node(_jac_here_, _Jac.edge_ref(self, _Jac.EdgeDir.OUT, None)):
            pass
        else:
            print("finished visitng all nodes  ....\n")


@_Jac.make_architype("node", on_entry=[], on_exit=[])
class node2:
    val2: int


_Jac.spawn_call(_Jac.get_root(), walker_1())
