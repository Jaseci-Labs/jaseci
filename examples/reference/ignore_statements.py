"""Testing ignore."""
from __future__ import annotations
from jaclang.plugin.feature import JacFeature as jac


@jac.make_architype(
    "walker", on_entry=[jac.DSFunc("start_game", jac.RootType)], on_exit=[]
)
class GuessGame:
    def start_game(self, walker_here: jac.RootType) -> None:
        i = 0
        while i < 10:
            jac.connect(
                walker_here, turn(), jac.build_edge(jac.EdgeDir.OUT, None, None)
            )
            i += 1
        if jac.visit_node(self, jac.edge_ref(walker_here, jac.EdgeDir.OUT, None)):
            pass


@jac.make_architype(
    "walker", on_entry=[jac.DSFunc("start_game", jac.RootType)], on_exit=[]
)
class GuessGame2:
    def start_game(self, walker_here: jac.RootType) -> None:
        i = 0
        while i < 10:
            jac.connect(
                walker_here, turn(), jac.build_edge(jac.EdgeDir.OUT, None, None)
            )
            i += 1
        i = 0
        while i < 15:
            jac.ignore(self, jac.edge_ref(walker_here, jac.EdgeDir.OUT, None)[i])
            i += 1
        if jac.visit_node(self, jac.edge_ref(walker_here, jac.EdgeDir.OUT, None)):
            pass


@jac.make_architype(
    "node", on_entry=[jac.DSFunc("check", GuessGame | GuessGame2)], on_exit=[]
)
class turn:
    def check(self, node_here: GuessGame | GuessGame2) -> None:
        print("here", end=", ")


jac.spawn_call(jac.get_root(), GuessGame())
print("")
jac.spawn_call(jac.get_root(), GuessGame2())
print("")
