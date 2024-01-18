import random


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
print((lambda x: [i for i in x if i.y <= 10])(apple))
