walker init {
    a = 4; b = 5;
    if(a == b): std.out("A equals B");
    elif(a > b): std.out("A is greater than B");
    elif(a == b - 1): std.out("A is one less than B");
    elif(a == b - 2): std.out("A is two less than B");
    else: std.out("A is something else");
}