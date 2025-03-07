from __future__ import annotations
from jaclang.plugin.feature import JacFeature as Jac


# Since the Animal class cannot be inherit from object, (cause the base class will be changed at run time)
# we need a base class.
#
# reference: https://stackoverflow.com/a/9639512/10846399
#
class Base:
    pass


@Jac.make_walker(on_entry=[Jac.DSFunc("self_destruct", None)], on_exit=[])
class Visitor(Base):
    def self_destruct(self, _jac_here_) -> None:
        print("get's here")
        Jac.disengage(self)
        return
        print("but not here")


Jac.spawn_call(Jac.get_root(), Visitor())
