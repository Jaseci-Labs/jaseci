glob x = 5, y = 2;

test a {
    check almostEqual(5, x);
}

test b {
    check "l" in "llm";
}

test c {
    check x - y == 3;
}

test d {
    check 1 == 2;
}
