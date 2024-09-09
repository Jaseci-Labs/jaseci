can:priv hash(func: Any) {
    can inner(a: Any) {
        print(("#" * 20));
        func(a);
        print(("#" * 20));
    }
    return inner;
}

can:protect exclaim(func: Any) {
    can inner(b: Any) {
        print(("!" * 20));
        func(b);
        print(("!" * 20));
    }
    return inner;
}

@hash
@exclaim
can greeter(name: Any) {
    print("Hello, " + name + "!");
}

with entry {
    greeter("World");
}
