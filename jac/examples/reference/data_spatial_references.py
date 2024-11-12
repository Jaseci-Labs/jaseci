from __future__ import annotations
from jaclang.plugin.feature import JacFeature as _Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass as __jac_dataclass__


@_Jac.make_walker(on_entry=[_Jac.DSFunc("create")], on_exit=[])
@__jac_dataclass__(eq=False)
class Creator(_Jac.Walker):

    @_Jac.impl_patch_filename(
        file_loc="c:\\Users\\thami\\OneDrive\\Desktop\\VirtualEnv\\JacEnv\\doing.jac"
    )
    def create(self, _jac_here_: _Jac.RootType) -> None:
        end = _jac_here_
        i = 0
        while i < 3:
            _Jac.connect(
                left=end,
                right=(end := node_a(val=i)),
                edge_spec=_Jac.build_edge(
                    is_undirected=False, conn_type=None, conn_assign=None
                ),
            )
            i += 1
        _Jac.connect(
            left=end,
            right=(end := node_a(val=i + 10)),
            edge_spec=_Jac.build_edge(
                is_undirected=False, conn_type=connector, conn_assign=(("value",), (i,))
            ),
        )
        _Jac.connect(
            left=(end := node_a(val=i + 10)),
            right=_Jac.get_root(),
            edge_spec=_Jac.build_edge(
                is_undirected=False, conn_type=connector, conn_assign=(("value",), (i,))
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


@_Jac.make_node(on_entry=[_Jac.DSFunc("make_something")], on_exit=[])
@__jac_dataclass__(eq=False)
class node_a(_Jac.Node):
    val: int

    @_Jac.impl_patch_filename(
        file_loc="c:\\Users\\thami\\OneDrive\\Desktop\\VirtualEnv\\JacEnv\\doing.jac"
    )
    def make_something(self, _jac_here_: Creator) -> None:
        i = 0
        while i < 5:
            print(f"wlecome to {self}")
            i += 1


@_Jac.make_edge(on_entry=[], on_exit=[])
@__jac_dataclass__(eq=False)
class connector(_Jac.Edge):
    value: int = _Jac.has_instance_default(gen_func=lambda: 10)


_Jac.spawn_call(_Jac.get_root(), Creator())
