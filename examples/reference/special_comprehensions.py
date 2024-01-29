from __future__ import annotations
from jaclang.plugin.feature import JacFeature as _Jac
import random


random.seed(42)

@_Jac.make_architype('obj', on_entry=[], on_exit=[])
class TestObj:

    def __init__(self) -> None:
        self.x = random.randint(0, 15)
        self.y = random.randint(0, 15)
        self.z = random.randint(0, 15)
    x: int = random.randint(0, 15)
    y: int = random.randint(0, 20)
    z: int = random.randint(0, 50)
apple = []
i = 0
while i < 10:
    apple.append(TestObj())
    i += 1
print((lambda x: [i for i in x if i.y <= 7])(apple))

@_Jac.make_architype('obj', on_entry=[], on_exit=[])
class MyObj:
    apple: int = 0
    banana: int = 0
x = MyObj()
y = MyObj()
mvar = _Jac.assign_compr([x, y], (('apple', 'banana'), (5, 7)))
print(mvar)