from __future__ import annotations
from jaclang.plugin.feature import JacFeature as Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass


@Jac.make_walker(on_entry=[Jac.DSFunc("produce")], on_exit=[])
@dataclass(eq=False)
class Producer(Jac.Walker):

    def produce(self, _jac_here_: Jac.RootType) -> None:
        end = _jac_here_
        i = 0
        while i <= 2:
            Jac.connect(
                left=end,
                right=(end := Product(number=i + 1)),
                edge_spec=Jac.build_edge(
                    is_undirected=False, conn_type=None, conn_assign=None
                ),
            )
            i += 1
        if Jac.visit_node(
            self,
            Jac.edge_ref(
                _jac_here_,
                target_obj=None,
                dir=Jac.EdgeDir.OUT,
                filter_func=None,
                edges_only=False,
            ),
        ):
            pass


@Jac.make_node(on_entry=[Jac.DSFunc("make")], on_exit=[])
@dataclass(eq=False)
class Product(Jac.Node):
    number: int

    def make(self, _jac_here_: Producer) -> None:
        print(f"Hi, I am {self} returning a String")
        if Jac.visit_node(
            _jac_here_,
            Jac.edge_ref(
                self,
                target_obj=None,
                dir=Jac.EdgeDir.OUT,
                filter_func=None,
                edges_only=False,
            ),
        ):
            pass


Jac.spawn_call(Jac.get_root(), Producer())
