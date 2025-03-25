with entry {
    a = b = 16;
    print(a);
    print(b);
}

with entry {
    a = 16;
    a >>= 2;# a becomes 4, equivalent to dividing by 2^2
    print(a);
}

with entry {
    a = 2;
    a <<= 2;# a becomes 16, equivalent to multiplying by 2^2
    print(a);
}

with entry {
    c = 18;
    c //= 4;# c becomes 4, equivalent to integer division of 18 by 4
    print(c);
}
