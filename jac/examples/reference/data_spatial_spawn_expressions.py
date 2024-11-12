from __future__ import annotations
from jaclang.plugin.feature import JacFeature as _Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass as __jac_dataclass__


@_Jac.make_walker(on_entry=[_Jac.DSFunc("do")], on_exit=[])
@__jac_dataclass__(eq=False)
class Adder(_Jac.Walker):

    @_Jac.impl_patch_filename(
        file_loc="c:\\Users\\thami\\OneDrive\\Desktop\\VirtualEnv\\JacEnv\\doing.jac"
    )
    def do(self, _jac_here_: _Jac.RootType) -> None:
        _Jac.connect(
            left=_jac_here_,
            right=node_a(),
            edge_spec=_Jac.build_edge(
                is_undirected=False, conn_type=None, conn_assign=None
            ),
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


@_Jac.make_node(on_entry=[_Jac.DSFunc("add")], on_exit=[])
@__jac_dataclass__(eq=False)
class node_a(_Jac.Node):
    x: int = _Jac.has_instance_default(gen_func=lambda: 0)
    y: int = _Jac.has_instance_default(gen_func=lambda: 0)

    @_Jac.impl_patch_filename(
        file_loc="c:\\Users\\thami\\OneDrive\\Desktop\\VirtualEnv\\JacEnv\\doing.jac"
    )
    def add(self, _jac_here_: Adder) -> None:
        self.x = 550
        self.y = 450
        print(int(self.x) + int(self.y))


_Jac.spawn_call(Adder(), _Jac.get_root())
