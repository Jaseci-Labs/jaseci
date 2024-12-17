from __future__ import annotations
from jaclang.plugin.feature import JacFeature as _Jac


# Since the Animal class cannot be inherit from object, (cause the base class will be changed at run time)
# we need a base class.
#
# reference: https://stackoverflow.com/a/9639512/10846399
#
class Base:
    pass


@_Jac.make_walker(on_entry=[_Jac.DSFunc("travel", _Jac.get_root_type())], on_exit=[])
class Visitor(Base):
    def travel(self, _jac_here_: _Jac.get_root_type()) -> None:
        if _Jac.visit_node(
            self, _Jac.edge_ref(_jac_here_, None, _Jac.EdgeDir.OUT, None, None)
        ):
            pass
        elif _Jac.visit_node(self, _Jac.get_root()):
            pass


@_Jac.make_node(on_entry=[_Jac.DSFunc("speak", Visitor)], on_exit=[])
class item(Base):
    def speak(self, _jac_here_: Visitor) -> None:
        print("Hey There!!!")
        _Jac.disengage(_jac_here_)
        return


i = 0
while i < 5:
    _Jac.connect(_Jac.get_root(), item(), _Jac.build_edge(_Jac.EdgeDir.OUT, None, None))
    i += 1
_Jac.spawn_call(_Jac.get_root(), Visitor())
