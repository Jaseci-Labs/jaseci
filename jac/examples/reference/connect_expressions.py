from __future__ import annotations
from jaclang.plugin.feature import JacFeature as _Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass as __jac_dataclass__


@_Jac.make_node(on_entry=[], on_exit=[])
@__jac_dataclass__(eq=False)
class node_a(_Jac.Node):
    value: int


@_Jac.make_walker(on_entry=[_Jac.DSFunc("create"), _Jac.DSFunc("travel")], on_exit=[])
@__jac_dataclass__(eq=False)
class Creator(_Jac.Walker):

    @_Jac.impl_patch_filename(
        file_loc="c:\\Users\\thami\\OneDrive\\Desktop\\VirtualEnv\\JacEnv\\doing.jac"
    )
    def create(self, _jac_here_: _Jac.RootType) -> None:
        end = _jac_here_
        i = 0
        while i < 7:
            if i % 2 == 0:
                _Jac.connect(
                    left=end,
                    right=(end := node_a(value=i)),
                    edge_spec=_Jac.build_edge(
                        is_undirected=False, conn_type=None, conn_assign=None
                    ),
                )
            else:
                _Jac.connect(
                    left=end,
                    right=(end := node_a(value=i + 10)),
                    edge_spec=_Jac.build_edge(
                        is_undirected=False,
                        conn_type=MyEdge,
                        conn_assign=(("val",), (i,)),
                    ),
                )
            i += 1

    @_Jac.impl_patch_filename(
        file_loc="c:\\Users\\thami\\OneDrive\\Desktop\\VirtualEnv\\JacEnv\\doing.jac"
    )
    def travel(self, _jac_here_: _Jac.RootType | node_a) -> None:
        for i in _Jac.edge_ref(
            _jac_here_,
            target_obj=None,
            dir=_Jac.EdgeDir.OUT,
            filter_func=lambda x: [i for i in x if isinstance(i, MyEdge) if i.val <= 6],
            edges_only=False,
        ):
            print(i.value)
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


@_Jac.make_edge(on_entry=[], on_exit=[])
@__jac_dataclass__(eq=False)
class MyEdge(_Jac.Edge):
    val: int = _Jac.has_instance_default(gen_func=lambda: 5)


if __name__ == "__main__":
    _Jac.spawn_call(_Jac.get_root(), Creator())
