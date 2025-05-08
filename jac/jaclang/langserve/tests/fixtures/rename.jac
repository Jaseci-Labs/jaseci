def foo;



impl def foo{
    print("foo");
}


obj out{
    has cnt :int;
    def bar;
    def baz;
}


impl can out.bar{
    print("bar");
}

impl can out.baz{
    print("baz");
}

with entry{
    foo();
    new = out();
    new.cnt;
    out(1).bar();
}