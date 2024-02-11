from __future__ import annotations
from enum import Enum, auto


class Color(Enum):
    RED = 1
    pencil = auto()
    print("text")


print(Color.RED.value)
