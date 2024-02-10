from enum import Enum, auto
from enumeration_bodies import *


class Color(Enum):
    RED = 1
    pencil = auto()
    print("text")


print(Color.RED.value)
