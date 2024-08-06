glob expected_area = 78.53981633974483;

test a1 {
    check almostEqual(calculate_area(RAD), expected_area);
}

test a2 {
    c = Circle(RAD);
    check almostEqual(c.area(), expected_area);
}

test a3 {
    c = Circle(RAD);
    check c.shape_type == ShapeType.CIRCLE;
}
