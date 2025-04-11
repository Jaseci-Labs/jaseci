from __future__ import annotations
from jaclang import *


@walker
class Producer:

    @with_entry
    def produce(self, here: Jac.RootType) -> None:
        end = here
        i = 0
        while i < 3:
            Jac.conn(end, (end := Product(number=i + 1)))
            i += 1
        Jac.visit(self, Jac.refs(here))


@node
class Product:
    number: int

    @with_entry
    def make(self, here: Producer) -> None:
        print(f"Hi, I am {self} returning a String")
        Jac.visit(here, Jac.refs(self))


Jac.spawn(root(), Producer())
