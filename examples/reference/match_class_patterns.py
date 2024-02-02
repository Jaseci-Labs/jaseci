from jaclang.plugin.feature import JacFeature as jac


@jac.make_obj(on_entry=[], on_exit=[])
class Point:
    x: float
    y: float


data = Point(x=9, y=0)
match data:
    case Point(int(a), y=0):
        print(f"Point with x={a} and y=0")
    case _:
        print("Not on the x-axis")
