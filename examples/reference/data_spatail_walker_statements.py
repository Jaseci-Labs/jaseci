from jaclang.plugin.feature import JacFeature as jac

@jac.make_architype('walker', on_entry=[jac.DSFunc('create', jac.RootType)], on_exit=[])
class walker_1:

    def create(self, walker_here: jac.RootType) -> None:
        end = walker_here
        i = 0
        while i < 5:
            jac.connect(end, (end := node_a(val=i + 1)), jac.build_edge(jac.EdgeDir.OUT, None, None))
            i += 1
        if jac.visit_node(self, jac.edge_ref(walker_here, jac.EdgeDir.OUT, None)):
            pass

@jac.make_architype('node', on_entry=[jac.DSFunc('print_something', walker_1)], on_exit=[])
class node_a:
    val: int

    def print_something(self, walker_here: walker_1) -> None:
        print(f'walker_1 entered to {self}')
        if jac.visit_node(walker_here, jac.edge_ref(self, jac.EdgeDir.OUT, None)):
            pass

@jac.make_architype('walker', on_entry=[jac.DSFunc('skip_root', jac.RootType), jac.DSFunc('do_something', node_a)], on_exit=[])
class walker_2:

    def skip_root(self, walker_here: jac.RootType) -> None:
        if jac.visit_node(self, jac.edge_ref(walker_here, jac.EdgeDir.OUT, None)):
            pass

    def do_something(self, walker_here: node_a) -> None:
        print(f'walker_2 reached to {walker_here}')
        if walker_here.val == 4:
            jac.disengage(self)
            return
        if jac.visit_node(self, jac.edge_ref(walker_here, jac.EdgeDir.OUT, None)):
            pass
        jac.ignore(self, [node_a(val=2)])
jac.spawn_call(walker_1(), jac.get_root())
jac.spawn_call(jac.get_root(), walker_2())