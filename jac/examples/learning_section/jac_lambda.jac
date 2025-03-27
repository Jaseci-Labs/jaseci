with entry {
    x = with a: int can a + 10;
    print(x(5));
}

with entry {
    x = with a: int, b: int can b + a;
    print(x(5, 4));
}

with entry {
    y = with a: int can a ** 2;
    print(y(6));
}
