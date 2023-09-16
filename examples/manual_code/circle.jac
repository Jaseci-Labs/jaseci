"""
(Module docstring are Required in a valid Jac)
This module demonstrates a simple circle class and a function to calculate the area of a circle.
"""
import:py math;

# Module-level global
global RADIUS = 5;

"""Function to calculate the area of a circle."""
can calculate_area(radius: float) -> float {
    return math.pi * radius * radius;
}

#* (This is multiline comments in Jac)
Above we have the demonstration of a function to calculate the area of a circle.
Below we have the demonstration of a class to calculate the area of a circle.
*#

"""Enum for shape types"""
enum ShapeType {
    CIRCLE = "Circle",
    UNKNOWN = "Unknown"
}

"""Base class for a shape."""
object Shape {
    has shape_type: ShapeType;

    can <init>(shape_type: ShapeType) {
        <self>.shape_type = shape_type;
    }

    """Abstract method to calculate the area of a shape."""
    can area -> float abstract;
}


object Circle(Shape) {
    """Circle class inherits from Shape."""

    can <init>(radius: float) {
        <super>.<init>(ShapeType.CIRCLE);
        self.radius = radius;
    }

    """Overridden method to calculate the area of the circle."""
    can area -> float {
        return math.pi * self.radius * self.radius;
    }
}

with entry {c = Circle(RADIUS);}  # Global also works here

with entry:__main__ { # TODO: add name == option abstract feature
    # To run the program functionality
    print(f"Area of a circle with radius 5: {calculate_area(RADIUS)}")
    print(f"Area of a {c.shape_type.value} with radius 5: {c.area()}")

}

# TODO: Make tests works
test calculate_area {
    expected_area = 78.53981633974483;
    assertAlmostEqual(calculate_area(RADIUS), expected_area);
}

test circle_area {
    c = Circle(RADIUS);
    expected_area = 78.53981633974483;
    assertAlmostEqual(c.area(), expected_area);
}

test circle_type {
    c = Circle(RADIUS);
    assertEqual(c.shape_type, ShapeType.CIRCLE);
}