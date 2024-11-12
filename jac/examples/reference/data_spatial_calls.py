from __future__ import annotations
from jaclang.plugin.feature import JacFeature as _Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass as __jac_dataclass__


@_Jac.make_walker(on_entry=[_Jac.DSFunc("func2")], on_exit=[])
@__jac_dataclass__(eq=False)
class Creator(_Jac.Walker):

    @_Jac.impl_patch_filename(
        file_loc="c:\\Users\\thami\\OneDrive\\Desktop\\VirtualEnv\\JacEnv\\doing.jac"
    )
    def func2(self, _jac_here_: _Jac.RootType) -> None:
        end = _jac_here_
        i = 0
        while i < 5:
            _Jac.connect(
                left=end,
                right=(end := node_1(val=i + 1)),
                edge_spec=_Jac.build_edge(
                    is_undirected=False, conn_type=None, conn_assign=None
                ),
            )
            i += 1
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


@_Jac.make_node(on_entry=[_Jac.DSFunc("func_1")], on_exit=[])
@__jac_dataclass__(eq=False)
class node_1(_Jac.Node):
    val: int

    @_Jac.impl_patch_filename(
        file_loc="c:\\Users\\thami\\OneDrive\\Desktop\\VirtualEnv\\JacEnv\\doing.jac"
    )
    def func_1(self, _jac_here_: Creator) -> None:
        print("visiting ", self)
        if _Jac.visit_node(
            _jac_here_,
            _Jac.edge_ref(
                self,
                target_obj=None,
                dir=_Jac.EdgeDir.OUT,
                filter_func=None,
                edges_only=False,
            ),
        ):
            pass


_Jac.spawn_call(_Jac.get_root(), Creator())
_Jac.spawn_call(_Jac.get_root(), Creator())
