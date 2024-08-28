can foo;



:can:foo{
    print("foo");
}


obj out{
    can bar;
}


:obj:out:can:bar{
    print("bar");
}


with entry{
    foo();
    out().bar();
}