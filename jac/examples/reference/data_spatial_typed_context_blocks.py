from __future__ import annotations
from jaclang import *

class Producer(Walker):

    @with_entry
    @Jac.impl_patch_filename('data_spatial_typed_context_blocks.jac')
    def produce(self, here: Root) -> None:
        end = here
        i = 0
        while i < 3:
            end.connect((end := Product(number=i + 1)))
            i += 1
        self.visit(here.refs())

class Product(Node):
    number: int

    @with_entry
    @Jac.impl_patch_filename('data_spatial_typed_context_blocks.jac')
    def make(self, here: Producer) -> None:
        print(f'Hi, I am {self} returning a String')
        here.visit(self.refs())
root.spawn(Producer())
