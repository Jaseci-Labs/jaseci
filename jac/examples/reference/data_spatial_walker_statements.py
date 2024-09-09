from __future__ import annotations
from jaclang.plugin.feature import JacFeature as _Jac


@_Jac.make_walker(on_entry=[_Jac.DSFunc("self_destruct", None)], on_exit=[])
class Visitor:
    def self_destruct(self, _jac_here_) -> None:
        print("get's here")
        _Jac.disengage(self)
        return
        print("but not here")


_Jac.spawn_call(_Jac.get_root(), Visitor())
