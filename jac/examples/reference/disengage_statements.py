from __future__ import annotations
from jaclang import *


class Visitor(Walker):
    @with_entry
    def travel(self, here: Root) -> None:
        if not self.visit(here.refs()):
            self.visit(root())


class item(Node):
    @with_entry
    def speak(self, here: Visitor) -> None:
        print("Hey There!!!")
        return here.disengage()


i = 0

while i < 5:
    root().connect(item())
    i += 1

root().spawn(Visitor())
