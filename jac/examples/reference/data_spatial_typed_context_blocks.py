from __future__ import annotations
from jaclang import *


@walker
class Producer:

    @with_entry
    def produce(self, here: Root) -> None:
        end = here
        i = 0
        while i < 3:
            end.connect((end := Product(number=i + 1)))
            i += 1
        self.visit(here.refs())


@node
class Product:
    number: int

    @with_entry
    def make(self, here: Producer) -> None:
        print(f"Hi, I am {self} returning a String")
        here.visit(self.refs())


root().spawn(Producer())
