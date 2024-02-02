from jaclang.plugin.feature import JacFeature as jac
import random


@jac.make_obj(on_entry=[], on_exit=[])
class TestObj:
    x: int = jac.has_instance_default(gen_func=lambda: random.randint(0, 15))
    y: int = jac.has_instance_default(gen_func=lambda: random.randint(0, 15))
    z: int = jac.has_instance_default(gen_func=lambda: random.randint(0, 15))


random.seed(42)
apple = []
i = 0
while i < 10:
    apple.append(TestObj())
    i += 1
print((lambda x: [i for i in x if i.y <= 7])(apple))


@jac.make_obj(on_entry=[], on_exit=[])
class MyObj:
    apple: int = jac.has_instance_default(gen_func=lambda: 0)
    banana: int = jac.has_instance_default(gen_func=lambda: 0)


x = MyObj()
y = MyObj()
mvar = jac.assign_compr([x, y], (("apple", "banana"), (5, 7)))
print(mvar)
