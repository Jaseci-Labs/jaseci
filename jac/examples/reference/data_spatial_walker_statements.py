from __future__ import annotations
from jaclang import *


@walker
class Visitor:

    @with_entry
    def self_destruct(self, here) -> None:
        print("get's here")
        return self.disengage()
        print("but not here")


root().spawn(Visitor())
