from jaclang.plugin.feature import JacFeature as jac


@jac.make_walker(on_entry=[jac.DSFunc("func2", jac.RootType)], on_exit=[])
class Creator:
    def func2(self, jac_here_: jac.RootType) -> None:
        end = jac_here_
        i = 0
        while i < 5:
            jac.connect(
                end,
                (end := node_1(val=i + 1)),
                jac.build_edge(jac.EdgeDir.OUT, None, None),
            )
            i += 1
        if jac.visit_node(self, jac.edge_ref(jac_here_, jac.EdgeDir.OUT, None, None)):
            pass


@jac.make_node(on_entry=[jac.DSFunc("func_1", Creator)], on_exit=[])
class node_1:
    val: int

    def func_1(self, jac_here_: Creator) -> None:
        print("visiting ", self)
        if jac.visit_node(jac_here_, jac.edge_ref(self, jac.EdgeDir.OUT, None, None)):
            pass


jac.spawn_call(jac.get_root(), Creator())
jac.spawn_call(jac.get_root(), Creator())
