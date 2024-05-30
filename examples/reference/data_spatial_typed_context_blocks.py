from __future__ import annotations
from jaclang.plugin.feature import JacFeature as Jac
from dataclasses import dataclass as dataclass


@Jac.make_walker(on_entry=[Jac.DSFunc("produce", Jac.get_root_type())], on_exit=[])
@dataclass(eq=False)
class Producer:

    def produce(self, here: Jac.get_root_type()) -> None:
        end = here
        i = 0
        while i <= 2:
            Jac.connect(
                end, (end := Product(number=i + 1)), Jac.build_edge(False, None, None)
            )
            i += 1
        if Jac.visit_node(
            self,
            Jac.edge_ref(here, None, Jac.EdgeDir.OUT, filter_func=None),
        ):
            pass


@Jac.make_node(on_entry=[Jac.DSFunc("make", Producer)], on_exit=[])
@dataclass(eq=False)
class Product:
    number: int

    def make(self, here: Producer) -> None:
        print(f"Hi, I am {self} returning a String")
        if Jac.visit_node(
            here,
            Jac.edge_ref(self, None, Jac.EdgeDir.OUT, filter_func=None),
        ):
            pass


Jac.spawn_call(Jac.get_root(), Producer())
