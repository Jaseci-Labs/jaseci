walker init {
    a=5;
    std.out(a.type, '-', a);
    a=5.0;
    std.out(a.type, '-', a);
    a=true;
    std.out(a.type, '-', a);
    a=[5];
    std.out(a.type, '-', a);
    a='5';
    std.out(a.type, '-', a);
    a={'num': 5};
    std.out(a.type, '-', a);
}