obj SomeObj {
    has a: int = 5;
}

with entry {
    ob = SomeObj();
    a = {ob: "check"};
    x=5;
    print(a[ob]);
    ob.a = 10;
    ob.b = 20;
    print(a[ob]);
}