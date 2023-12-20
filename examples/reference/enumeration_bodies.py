from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


def print_color(color):
    if color == Color.RED:
        print("It's red!")
    elif color == Color.GREEN:
        print("It's green!")
    elif color == Color.BLUE:
        print("It's blue!")


print(Color.RED)  # Output: Color.RED
print(Color.RED.value)  # Output: 1

for color in Color:
    print(color)

if Color.RED == Color.BLUE:
    print("Colors are the same")
else:
    print("Colors are different")  # Output: Colors are different

print_color(Color.GREEN)  # Output: It's green!
