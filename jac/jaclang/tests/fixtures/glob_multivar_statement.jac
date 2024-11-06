glob a: str, b: str;
glob c: str;

can do() {
    :g: a, b, c ;

    a = "Welcome";
    b = "to";
    c = "Jaseci!";
}

with entry {
    a = "Hello";
    b = "World";
    c = "!";
    print(a, b, c);
    do();
    print(a, b, c);
}
