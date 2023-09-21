"""Enum for shape types"""

:enum:ShapeType {
    CIRCLE = "Circle",
    UNKNOWN = "Unknown"
}

"""Function to calculate the area of a circle."""
:ability:calculate_area
(radius: float) -> float {
    return math.pi * radius * radius;
}

:object:Circle:ability:<init> {
    <super>.<init>(ShapeType.CIRCLE);
}

"""Overridden method to calculate the area of the circle."""
:object:Circle:ability:area -> float {
    return math.pi * self.radius * self.radius;
}

:ability:main_run {
    print(f"Area of a circle with radius {RAD} using function: {calculate_area(RAD)}");
    print(f"Area of a {c.shape_type.value} with radius {RAD} using class: {c.area()}");
}

