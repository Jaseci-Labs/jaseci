glob a = 5, b = 2;

test t1 {
    check assertAlmostEqual(a, 6);
}

test t2 {
    check assertTrue(a != b);
}

test t3 {
    check assertIn("d", "abc");
}

test t4 {
    check assertEqual(a - b, 3);
}
