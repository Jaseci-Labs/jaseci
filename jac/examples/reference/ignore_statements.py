from __future__ import annotations
from jaclang.plugin.feature import JacFeature as _Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass as __jac_dataclass__


@_Jac.make_walker(on_entry=[_Jac.DSFunc("travel")], on_exit=[])
@__jac_dataclass__(eq=False)
class Visitor(_Jac.Walker):

    def travel(self, _jac_here_: _Jac.RootType) -> None:
        _Jac.ignore(
            self,
            _Jac.edge_ref(
                _jac_here_,
                target_obj=None,
                dir=_Jac.EdgeDir.OUT,
                filter_func=None,
                edges_only=False,
            )[0],
        )
        if _Jac.visit_node(
            self,
            _Jac.edge_ref(
                _jac_here_,
                target_obj=None,
                dir=_Jac.EdgeDir.OUT,
                filter_func=None,
                edges_only=False,
            ),
        ):
            pass
        else:
            visitroot


@_Jac.make_node(on_entry=[_Jac.DSFunc("speak")], on_exit=[])
@__jac_dataclass__(eq=False)
class item(_Jac.Node):

    def speak(self, _jac_here_: Visitor) -> None:
        print("Hey There!!!")


i = 0
while i < 5:
    _Jac.connect(
        left=_Jac.get_root(),
        right=item(),
        edge_spec=_Jac.build_edge(
            is_undirected=False, conn_type=None, conn_assign=None
        ),
    )
    i += 1
_Jac.spawn_call(_Jac.get_root(), Visitor())
