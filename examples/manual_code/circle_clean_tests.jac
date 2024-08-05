include:jac circle_clean;

glob expected_area = 78.53981633974483;

test {
    check almostEqual(calculate_area(RAD), expected_area);
}

test {
    c = Circle(RAD);
    check almostEqual(c.area(), expected_area);
}

test {
    c = Circle(RAD);
    check c.shape_type == ShapeType.CIRCLE;
}
