from __future__ import annotations
from jaclang.plugin.feature import JacFeature as jac

@jac.make_architype('walker', on_entry=[jac.DSFunc('start_game', jac.RootType)], on_exit=[])
class GuessGame:

    def start_game(self, _jac_here_: jac.RootType) -> None:
        i = 0
        while i < 10:
            jac.connect(_jac_here_, turn(), jac.build_edge(jac.EdgeDir.OUT, None, None))
            i += 1
        i = 0
        while i < 5:
            jac.ignore(self, jac.edge_ref(_jac_here_, jac.EdgeDir.OUT, None, None)[i])
            i += 1
        if jac.visit_node(self, jac.edge_ref(_jac_here_, jac.EdgeDir.OUT, None, None)):
            pass

@jac.make_architype('node', on_entry=[jac.DSFunc('check', GuessGame)], on_exit=[])
class turn:

    def check(self, _jac_here_: GuessGame) -> None:
        print('here', end=', ')
jac.spawn_call(jac.get_root(), GuessGame())