from __future__ import annotations
from jaclang.plugin.feature import JacFeature as Jac
from dataclasses import dataclass as dataclass
import random


# Since the Jac class cannot be inherit from object, (cause the base class will be changed at run time)
# we need a base class.
#
# reference: https://stackoverflow.com/a/9639512/10846399
#
class Base:
    pass


@Jac.make_obj(on_entry=[], on_exit=[])
@dataclass(eq=False)
class TestObj(Base):
    x: int = Jac.has_instance_default(gen_func=lambda: random.randint(0, 15))
    y: int = Jac.has_instance_default(gen_func=lambda: random.randint(0, 15))
    z: int = Jac.has_instance_default(gen_func=lambda: random.randint(0, 15))


random.seed(42)
apple = []
i = 0
while i < 10:
    apple.append(TestObj())
    i += 1
print((lambda x: [i for i in x if i.y <= 7])(apple))


@Jac.make_obj(on_entry=[], on_exit=[])
@dataclass(eq=False)
class MyObj(Base):
    apple: int = Jac.has_instance_default(gen_func=lambda: 0)
    banana: int = Jac.has_instance_default(gen_func=lambda: 0)


x = MyObj()
y = MyObj()
mvar = Jac.assign_compr([x, y], (("apple", "banana"), (5, 7)))
print(mvar)
