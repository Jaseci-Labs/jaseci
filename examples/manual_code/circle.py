"""
This module demonstrates a simple circle class and a function to calculate the area of a circle.
(Module docstrings are optional but good practice in python)
"""
from enum import Enum
import math
import unittest

# Module-level global
RADIUS = 5


def calculate_area(radius: float) -> float:
    """Function to calculate the area of a circle."""
    return math.pi * radius * radius


# Multiline comments in python feels like a hack
"""
Above we have the demonstration of a function to calculate the area of a circle.
Below we have the demonstration of a class to calculate the area of a circle.
"""


# Enum for shape types
class ShapeType(Enum):
    CIRCLE = "Circle"
    UNKNOWN = "Unknown"


class Shape:
    """Base class for a shape."""

    def __init__(self, shape_type: ShapeType):
        self.shape_type = shape_type

    def area(self) -> float:
        """Returns the area of the shape."""
        pass


class Circle(Shape):
    """Circle class inherits from Shape."""

    def __init__(self, radius: float):
        super().__init__(ShapeType.CIRCLE)
        self.radius = radius

    def area(self) -> float:
        """Overridden method to calculate the area of the circle."""
        return math.pi * self.radius * self.radius


c = Circle(RADIUS)

if __name__ == "__main__":
    # To run the program functionality
    print(
        f"Area of a circle with radius {RADIUS} using function: {calculate_area(RADIUS)}"
    )
    print(
        f"Area of a {c.shape_type.value} with radius {RADIUS} using class: {c.area()}"
    )

    # Uncomment the next line if you want to run the unit tests
    # run_tests()


# Unit tests below, bad practice in python to have unit tests in the same file as the code
class TestShapesFunctions(unittest.TestCase):
    def test_calculate_area(self):
        expected_area = 78.53981633974483
        self.assertAlmostEqual(calculate_area(RADIUS), expected_area)

    def test_circle_area(self):
        c = Circle(RADIUS)
        expected_area = 78.53981633974483
        self.assertAlmostEqual(c.area(), expected_area)

    def test_circle_type(self):
        c = Circle(RADIUS)
        self.assertEqual(c.shape_type, ShapeType.CIRCLE)
