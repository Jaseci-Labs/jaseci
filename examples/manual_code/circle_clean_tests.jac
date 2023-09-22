include:jac circle_clean;

global expected_area = 78.53981633974483;
test { check.AlmostEqual(calculate_area(RAD), expected_area); }
test { c = Circle(RAD); check.AlmostEqual(c.area(), expected_area); }
test { c = Circle(RAD); check.Equal(c.shape_type, ShapeType.CIRCLE); }