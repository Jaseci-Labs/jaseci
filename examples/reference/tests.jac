glob r=5, x =10, y=5, z=5;

can foo(a: float) -> float {
    return a *2;
}

test test1 { check.AlmostEqual(foo(r), x); }
test test2 { check.Equal(y, z); }
test test3 { check.Greater(38,4); }

with entry{
    print(test1());
    print(test2());
    print(test3());
}