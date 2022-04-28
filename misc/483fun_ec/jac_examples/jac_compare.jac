walker init {
    a = 5; b = 6;
    std.out(a == b,
            a != b,
            a < b,
            a > b,
            a <= b,
            a >= b,
            a == b-1);
}
