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

:object:Shape:ability:<init>
(shape_type: ShapeType) {
    <self>.shape_type = shape_type;
}

:object:Circle:ability:<init>
(radius: float) {
    <super>.<init>(ShapeType.CIRCLE);
    self.radius = radius;
}

"""Overridden method to calculate the area of the circle."""
:object:Circle:ability:area -> float {
    return math.pi * self.radius * self.radius;
}

:ability:main_run {
    print(f"Area of a circle with radius {RAD} using function: {calculate_area(RAD)}");
    print(f"Area of a {c.shape_type.value} with radius {RAD} using class: {c.area()}");
}

# Unit Tests!
global expected_area = 78.53981633974483;
test calculate_area { check.AlmostEqual(calculate_area(RAD), expected_area); }
test circle_area { c = Circle(RAD); check.AlmostEqual(c.area(), expected_area); }
test circle_type { c = Circle(RAD); check.Equal(c.shape_type, ShapeType.CIRCLE); }