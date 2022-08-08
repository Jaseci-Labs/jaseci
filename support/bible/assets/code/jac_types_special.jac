walker init {
    a=null;
    std.out(a.type, '-', a);
    a=str;
    std.out(a.type, '-', a);
    std.out(null.type);
    std.out(null.type.type);
}