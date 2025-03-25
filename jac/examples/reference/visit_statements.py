from __future__ import annotations
from jaclang import *


@walker
class Visitor:
    @with_entry
    def travel(self, here: Root) -> None:
        if not self.visit(here.refs()):
            self.visit(root())
            return self.disengage()


@node
class item:
    @with_entry
    def speak(self, here: Visitor) -> None:
        print("Hey There!!!")


i = 0
while i < 5:
    root().connect(item())
    i += 1

root().spawn(Visitor())
