walker init {
    a=5.6;
    std.out(a+2);
    std.out((a+2).int);
    std.out((a+2).str);
    std.out((a+2).bool);
    std.out((a+2).int.float);

    if(a.str.type == str and !(a.int.type == str) and a.int.type == int):
        std.out("Types comes back correct");
}
