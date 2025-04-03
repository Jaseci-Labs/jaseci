from __future__ import annotations
from jaclang import *
import typing

if typing.TYPE_CHECKING:
    import random
else:
    (random,) = jac_import("random", "py")


@obj
class TestObj:
    x: int = field(gen=lambda: random.randint(0, 15))
    y: int = field(gen=lambda: random.randint(0, 15))
    z: int = field(gen=lambda: random.randint(0, 15))


random.seed(42)
apple = JacList([])
i = 0
while i < 10:
    apple.append(TestObj())
    i += 1
print(apple.filter(None, lambda item: item.y <= 7))


@obj
class MyObj:
    apple: int = field(0)
    banana: int = field(0)


x = MyObj()
y = MyObj()
mvar = JacList([x, y]).assign(("apple", "banana"), (5, 7))
print(mvar)
