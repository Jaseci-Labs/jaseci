glob a = 5, b = 2;

test test1 {
    check assertAlmostEqual(a, 6);
}

test test2 {
    check assertTrue(a != b);
}

test test3 {
    check assertIn("d", "abc");
}

test test4 {
    check assertEqual(a - b, 3);
}