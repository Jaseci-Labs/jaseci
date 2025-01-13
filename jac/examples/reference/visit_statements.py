from __future__ import annotations
from jaclang.plugin.feature import JacFeature as Jac


# Since the Animal class cannot be inherit from object, (cause the base class will be changed at run time)
# we need a base class.
#
# reference: https://stackoverflow.com/a/9639512/10846399
#
class Base:
    pass


@Jac.make_walker(on_entry=[Jac.DSFunc("travel", Jac.get_root_type())], on_exit=[])
class Visitor(Base):
    def travel(self, _jac_here_: Jac.get_root_type()) -> None:
        if Jac.visit_node(
            self, Jac.edge_ref(_jac_here_, None, Jac.EdgeDir.OUT, None, None)
        ):
            pass
        elif Jac.visit_node(self, Jac.get_root()):
            pass


@Jac.make_node(on_entry=[Jac.DSFunc("speak", Visitor)], on_exit=[])
class item(Base):
    def speak(self, _jac_here_: Visitor) -> None:
        print("Hey There!!!")


i = 0
while i < 5:
    Jac.connect(Jac.get_root(), item(), Jac.build_edge(Jac.EdgeDir.OUT, None, None))
    i += 1
Jac.spawn_call(Jac.get_root(), Visitor())
