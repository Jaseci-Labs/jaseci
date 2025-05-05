obj A {
    has str_obj: str;
    has str_obj: float;
    has int_obj: int;

}

can func() -> A {
    return A();
}

with entry{
    a = A(23);
    b: A = a;
    b = func();
    c: int = a;
    a = 7;
}

obj B {
    can __init__(c: int) {

    }
}

with entry {
    b0 = B();
    b1 = B(1);
    b2 = B("1");
    b3 = B(B(1));
}