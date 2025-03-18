from __future__ import annotations
from jaclang import *


class Creator(Walker):

    @with_entry
    def func2(self, here: Root) -> None:
        end = here
        i = 0
        while i < 5:
            end.connect((end := node_1(val=i + 1)))
            i += 1
        self.visit(here.refs())


class node_1(Node):
    val: int

    @with_entry
    def func_1(self, here: Creator) -> None:
        print("visiting ", self)
        here.visit(self.refs())


root().spawn(Creator())
root().spawn(Creator())
