glob x = 5, y = 2;

test a {
    check assertAlmostEqual(5, x);
}

test b {
    check assertIn("l", "llm");
}

test c {
    check assertEqual(x - y, 3);
}

test d {
    check assertEqual(1, 2);
}
