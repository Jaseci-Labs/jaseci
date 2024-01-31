from jaclang.plugin.feature import JacFeature as jac


@jac.make_architype("walker", on_entry=[jac.DSFunc("create", jac.RootType)], on_exit=[])
class Creator:
    def create(self, Creator_here: jac.RootType) -> None:
        end = Creator_here
        i = 0
        while i <= 4:
            jac.connect(
                end,
                (end := leaf(val=i + 1)),
                jac.build_edge(jac.EdgeDir.OUT, None, None),
            )
            i += 1
        if jac.visit_node(
            self, jac.edge_ref(Creator_here, jac.EdgeDir.OUT, None, None)
        ):
            pass


@jac.make_architype("node", on_entry=[jac.DSFunc("print", Creator)], on_exit=[])
class leaf:
    val: int

    def print(self, leaf_here: Creator) -> None:
        print(f"This is {leaf_here} walk along {self}")
        if self.val == 4:
            print("walking stopped!!!")
            jac.disengage(leaf_here)
            return
        if jac.visit_node(leaf_here, jac.edge_ref(self, jac.EdgeDir.OUT, None, None)):
            pass


jac.spawn_call(jac.get_root(), Creator())
