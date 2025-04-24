from dataclasses import dataclass


@dataclass
class Inner:
    x: int
    y: int


@dataclass
class Container:
    inner: Inner


a = 1
b = 2

match Container(inner=Inner(x=a, y=b)):
    case Container(inner=Inner(x=val_x, y=0)):
        print(f"1.Inner.x={val_x}, Inner.y=0")
    case Container(inner=Inner(x=0, y=val_y)):
        print(f"2.Inner.x=0, Inner.y={val_y}")
    case Container(inner=Inner(x=val_x, y=val_y)):
        print(f"4.Inner.x={val_x}, Inner.y={val_y}")
    case _:
        print("5.No match")
