from __future__ import annotations
from jaclang.plugin.feature import JacFeature as _Jac

@_Jac.make_architype('walker', on_entry=[_Jac.DSFunc('create', _Jac.RootType)], on_exit=[])
class creator:

    def create(self, _jac_here_: _Jac.RootType) -> None:
        end = _jac_here_
        i = 0
        while i < 5:
            _Jac.connect(end, (end := item(val=i + 1)), _Jac.build_edge(_Jac.EdgeDir.OUT, None, None))
            i += 1
        if _Jac.visit_node(self, _Jac.edge_ref(_jac_here_, _Jac.EdgeDir.OUT, None, None)):
            pass

@_Jac.make_architype('walker', on_entry=[_Jac.DSFunc('func_3', _Jac.RootType)], on_exit=[])
class Travellor:

    def func_3(self, _jac_here_: _Jac.RootType) -> None:
        if _Jac.visit_node(self, item(val=2)):
            pass

@_Jac.make_architype('node', on_entry=[_Jac.DSFunc('func_1', creator | Travellor)], on_exit=[])
class item:
    val: int

    def func_1(self, _jac_here_: creator | Travellor) -> None:
        print('visiting ', self)
        if self.val == 2 and str(_jac_here_) == 'Travellor()':
            print('visiting again a specific node by w2\n')
        if _Jac.visit_node(_jac_here_, _Jac.edge_ref(self, _Jac.EdgeDir.OUT, None, None)):
            pass
        else:
            print('finished visitng all nodes  ....\n')
_Jac.spawn_call(_Jac.get_root(), creator())
_Jac.spawn_call(_Jac.get_root(), Travellor())