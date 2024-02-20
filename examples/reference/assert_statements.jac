can foo(value: int) {
    assert value > 0 , "Value must be positive";
}

with entry {
    try  {
        foo(-5);
    } except AssertionError as e  {
        print("Asserted:", e);
    }
}
