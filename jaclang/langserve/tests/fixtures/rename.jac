can foo;



:can:foo{
    print("foo");
}


obj out{
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
    out().bar();
}