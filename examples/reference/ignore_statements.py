"""Testing ignore."""
from __future__ import annotations
from jaclang.plugin.feature import JacFeature as _Jac


@_Jac.make_architype(
    "walker", on_entry=[_Jac.DSFunc("start_game", _Jac.RootType)], on_exit=[]
)
class GuessGame:
    def start_game(self, _jac_here_: _Jac.RootType) -> None:
        i = 0
        while i < 10:
            _Jac.connect(
                _jac_here_, turn(), _Jac.build_edge(_Jac.EdgeDir.OUT, None, None)
            )
            i += 1
        if _Jac.visit_node(self, _Jac.edge_ref(_jac_here_, _Jac.EdgeDir.OUT, None)):
            pass


@_Jac.make_architype(
    "walker", on_entry=[_Jac.DSFunc("start_game", _Jac.RootType)], on_exit=[]
)
class GuessGame2:
    def start_game(self, _jac_here_: _Jac.RootType) -> None:
        i = 0
        while i < 10:
            _Jac.connect(
                _jac_here_, turn(), _Jac.build_edge(_Jac.EdgeDir.OUT, None, None)
            )
            i += 1
        i = 0
        while i < 15:
            _Jac.ignore(self, _Jac.edge_ref(_jac_here_, _Jac.EdgeDir.OUT, None)[i])
            i += 1
        if _Jac.visit_node(self, _Jac.edge_ref(_jac_here_, _Jac.EdgeDir.OUT, None)):
            pass


@_Jac.make_architype(
    "node", on_entry=[_Jac.DSFunc("check", GuessGame | GuessGame2)], on_exit=[]
)
class turn:
    def check(self, _jac_here_: GuessGame | GuessGame2) -> None:
        print("here", end=", ")


_Jac.spawn_call(_Jac.get_root(), GuessGame())
print("")
_Jac.spawn_call(_Jac.get_root(), GuessGame2())
print("")
