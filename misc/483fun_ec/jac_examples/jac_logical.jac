walker init {
    a = true; b = false;
    std.out(a,
            !a,
            a && b,
            a || b,
            a and b,
            a or b,
            !a or b,
            !(a and b));
}