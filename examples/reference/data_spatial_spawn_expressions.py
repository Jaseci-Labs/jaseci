from jaclang.plugin.feature import JacFeature as jac


@jac.make_walker(on_entry=[jac.DSFunc("do", jac.get_root_type())], on_exit=[])
class Adder:
    def do(self, jac_here_: jac.get_root_type()) -> None:
        jac.connect(jac_here_, node_a(), jac.build_edge(jac.EdgeDir.OUT, None, None))
        if jac.visit_node(
            self, jac.edge_ref(jac_here_, None, jac.EdgeDir.OUT, None, None)
        ):
            pass


@jac.make_node(on_entry=[jac.DSFunc("add", Adder)], on_exit=[])
class node_a:
    x: int = jac.has_instance_default(gen_func=lambda: 0)
    y: int = jac.has_instance_default(gen_func=lambda: 0)

    def add(self, jac_here_: Adder) -> None:
        self.x = 550
        self.y = 450
        print(int(self.x) + int(self.y))


jac.spawn_call(Adder(), jac.get_root())
