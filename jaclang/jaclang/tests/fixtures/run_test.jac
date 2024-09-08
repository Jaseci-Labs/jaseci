glob a = 5, b = 2;

test t1 {
    check almostEqual(a, 6);
}

test t2 {
    check a != b;
}

test t3 {
    check "d" in "abc";
}

test t4 {
    check a - b == 3;
}
