can hash(func: Any) {
    can inner(a: Any) {
        print(("#" * 20));
        func(a);
        print(("#" * 20));
    }
    return inner;
}

can exclaim(func: Any) {
    can inner(b: Any) {
        print(("!" * 20));
        func(b);
        print(("!" * 20));
    }
    return inner;
}

can tilde(func: Any) {
    can inner(c: Any) {
        print(("~" * 20));
        func(c);
        print(("~" * 20));
    }
    return inner;
}

@hash
@exclaim
@tilde
can greeter(name: Any) {
    print("Hello, " + name + "!");
}

with entry {
    greeter("World");
}