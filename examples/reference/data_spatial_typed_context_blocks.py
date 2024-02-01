from jaclang.plugin.feature import JacFeature as jac


@jac.make_architype(
    "walker", on_entry=[jac.DSFunc("produce", jac.RootType)], on_exit=[]
)
class Producer:
    def produce(self, Producer_here: jac.RootType) -> None:
        end = Producer_here
        i = 0
        while i <= 2:
            jac.connect(
                end,
                (end := Product(number=i + 1)),
                jac.build_edge(jac.EdgeDir.OUT, None, None),
            )
            i += 1
        if jac.visit_node(
            self, jac.edge_ref(Producer_here, jac.EdgeDir.OUT, None, None)
        ):
            pass


@jac.make_architype("node", on_entry=[jac.DSFunc("make", Producer)], on_exit=[])
class Product:
    number: int

    def make(self, Product_here: Producer) -> None:
        print(f"Hi, I am {self} returning a String")
        if jac.visit_node(
            Product_here, jac.edge_ref(self, jac.EdgeDir.OUT, None, None)
        ):
            pass


jac.spawn_call(jac.get_root(), Producer())
