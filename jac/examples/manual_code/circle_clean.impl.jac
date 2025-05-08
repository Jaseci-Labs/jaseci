"""Enum for shape types"""

import math;

impl enum ShapeType {
    CIRCLE="Circle",
    UNKNOWN="Unknown"
}

"""Function to calculate the area of a circle."""
impl def calculate_area
(radius: float) -> float {
    return math.pi * radius * radius;
}

impl def Circle.init
(radius: float) {
    self.radius = radius;
    super.init(ShapeType.CIRCLE);
}

"""Overridden method to calculate the area of the circle."""
impl def Circle.area -> float {
    return math.pi * self.radius * self.radius;
}

impl def main_run {
    print(f"Area of a circle with radius {RAD} using function: {calculate_area(RAD)}");
    print(f"Area of a {c.shape_type.value} with radius {RAD} using class: {c.area()}");
}
