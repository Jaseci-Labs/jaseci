from __future__ import annotations
from jaclang.plugin.feature import JacFeature as _Jac


# Since the Jac class cannot be inherit from object, (cause the base class will be changed at run time)
# we need a base class.
#
# reference: https://stackoverflow.com/a/9639512/10846399
#
class Base:
    pass


@_Jac.make_walker(on_entry=[_Jac.DSFunc("self_destruct", None)], on_exit=[])
class Visitor(Base):
    def self_destruct(self, _jac_here_) -> None:
        print("get's here")
        _Jac.disengage(self)
        return
        print("but not here")


_Jac.spawn_call(_Jac.get_root(), Visitor())
