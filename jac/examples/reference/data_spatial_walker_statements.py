from __future__ import annotations
from jaclang import *

# Since the Animal class cannot be inherit from object, (cause the base class will be changed at run time)
# we need a base class.

# reference: https://stackoverflow.com/a/9639512/10846399

class Visitor(Walker):

    @with_entry
    def self_destruct(self, here) -> None:
        print("get's here")
        return self.disengage()
        print('but not here')
        
root.spawn(Visitor())
