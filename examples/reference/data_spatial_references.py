from __future__ import annotations
from jaclang.plugin.feature import JacFeature as Jac
from dataclasses import dataclass


@Jac.make_walker(on_entry=[Jac.DSFunc("create", Jac.get_root_type())], on_exit=[])
@dataclass(eq=False)
class Creator:

    def create(self, here: Jac.get_root_type()) -> None:
        end = here
        i = 0
        while i < 3:
            Jac.connect(end, (end := node_a(val=i)), Jac.build_edge(False, None, None))
            i += 1
        Jac.connect(
            end,
            (end := node_a(val=i + 10)),
            Jac.build_edge(False, connector, (("value",), (i,))),
        )
        Jac.connect(
            (end := node_a(val=i + 10)),
            Jac.get_root(),
            Jac.build_edge(False, connector, (("value",), (i,))),
        )
        if Jac.visit_node(
            self,
            Jac.edge_ref(here, None, Jac.EdgeDir.OUT, filter_func=None),
        ):
            pass


@Jac.make_node(on_entry=[Jac.DSFunc("make_something", Creator)], on_exit=[])
@dataclass(eq=False)
class node_a:
    val: int

    def make_something(self, here: Creator) -> None:
        i = 0
        while i < 5:
            print(f"wlecome to {self}")
            i += 1


@Jac.make_edge(on_entry=[], on_exit=[])
@dataclass(eq=False)
class connector:
    value: int = Jac.has_instance_default(gen_func=lambda: 10)


Jac.spawn_call(Jac.get_root(), Creator())
