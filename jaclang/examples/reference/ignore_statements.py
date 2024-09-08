from __future__ import annotations
from jaclang.plugin.feature import JacFeature as jac


@jac.make_walker(on_entry=[jac.DSFunc("travel", jac.get_root_type())], on_exit=[])
class Visitor:
    def travel(self, jac_here_: jac.get_root_type()) -> None:
        jac.ignore(self, jac.edge_ref(jac_here_, None, jac.EdgeDir.OUT, None, None)[0])
        if jac.visit_node(
            self, jac.edge_ref(jac_here_, None, jac.EdgeDir.OUT, None, None)
        ):
            pass
        elif jac.visit_node(self, jac.get_root()):
            pass


@jac.make_node(on_entry=[jac.DSFunc("speak", Visitor)], on_exit=[])
class item:
    def speak(self, jac_here_: Visitor) -> None:
        print("Hey There!!!")


i = 0
while i < 5:
    jac.connect(jac.get_root(), item(), jac.build_edge(jac.EdgeDir.OUT, None, None))
    i += 1
jac.spawn_call(jac.get_root(), Visitor())
