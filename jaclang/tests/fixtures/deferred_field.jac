obj SomeObj {
    has a: int = 5, b: int by <pi>;

    can <pi> {
        <self>.b = <self>.a * 3;
    }
}

with entry {
    ob = SomeObj();
    print(ob.a, ob.b);
}