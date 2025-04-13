from __future__ import annotations
from jaclang import *


@walker
class Visitor:

    @with_entry
    def self_destruct(self, here) -> None:
        print("get's here")
        return Jac.disengage(self)
        print("but not here")


Jac.spawn(root(), Visitor())
