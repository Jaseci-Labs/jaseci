glob a = 5, b = 2;

test test1 {
    check almostEqual(a, 6);
}

test test2 {
    check a != b;
}

test test3 {
    check "d" in "abc";
}

test test4 {
    check a - b == 3;
}