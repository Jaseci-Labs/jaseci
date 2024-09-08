can foo;



:can:foo{
    print("foo");
}


obj out{
    has cnt :int;
    can bar;
    can baz;
}


:obj:out:can:bar{
    print("bar");
}

:obj:out:can:baz{
    print("baz");
}

with entry{
    foo();
    new = out();
    new.cnt;
    out(1).bar();
}