from __future__ import annotations
from jaclang import *


class Visitor(Walker):

    @with_entry
    def self_destruct(self, here) -> None:
        print("get's here")
        return self.disengage()
        print("but not here")


root().spawn(Visitor())
