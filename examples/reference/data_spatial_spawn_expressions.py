from jaclang.plugin.feature import JacFeature as jac


@jac.make_architype("walker", on_entry=[jac.DSFunc("do", jac.RootType)], on_exit=[])
class Adder:
    def do(self, Adder_here: jac.RootType) -> None:
        jac.connect(Adder_here, node_a(), jac.build_edge(jac.EdgeDir.OUT, None, None))
        if jac.visit_node(self, jac.edge_ref(Adder_here, jac.EdgeDir.OUT, None, None)):
            pass


@jac.make_architype("node", on_entry=[jac.DSFunc("add", Adder)], on_exit=[])
class node_a:
    x: int = jac.has_instance_default(gen_func=lambda: 0)
    y: int = jac.has_instance_default(gen_func=lambda: 0)

    def add(self, node_here: Adder) -> None:
        self.x = 550
        self.y = 450
        print(int(self.x) + int(self.y))


jac.spawn_call(Adder(), jac.get_root())
