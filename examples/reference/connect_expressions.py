from jaclang.plugin.feature import JacFeature as jac


@jac.make_node(on_entry=[], on_exit=[])
class node_a:
    value: int


@jac.make_walker(
    on_entry=[
        jac.DSFunc("create", jac.RootType),
        jac.DSFunc("travel", jac.RootType | node_a),
    ],
    on_exit=[],
)
class Creator:
    def create(self, creator_here: jac.RootType) -> None:
        end = creator_here
        i = 0
        while i < 7:
            if i % 2 == 0:
                jac.connect(
                    end,
                    (end := node_a(value=i)),
                    jac.build_edge(jac.EdgeDir.OUT, None, None),
                )
            else:
                jac.connect(
                    end,
                    (end := node_a(value=i + 10)),
                    jac.build_edge(jac.EdgeDir.OUT, MyEdge, (("val",), (i,))),
                )
            i += 1

    def travel(self, creator_here: jac.RootType | node_a) -> None:
        for i in jac.edge_ref(
            creator_here,
            jac.EdgeDir.OUT,
            MyEdge,
            lambda x: [i for i in x if i.val <= 6],
        ):
            print(i.value)
        if jac.visit_node(
            self, jac.edge_ref(creator_here, jac.EdgeDir.OUT, None, None)
        ):
            pass


@jac.make_edge(on_entry=[], on_exit=[])
class MyEdge:
    val: int = jac.has_instance_default(gen_func=lambda: 5)


jac.spawn_call(jac.get_root(), Creator())
