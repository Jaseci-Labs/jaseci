include:jac circle_clean;

glob expected_area = 78.53981633974483;

test {
    check assertAlmostEqual(calculate_area(RAD), expected_area);
}

test {
    c = Circle(RAD);
    check assertAlmostEqual(c.area(), expected_area);
}

test {
    c = Circle(RAD);
    check assertEqual(c.shape_type, ShapeType.CIRCLE);
}
