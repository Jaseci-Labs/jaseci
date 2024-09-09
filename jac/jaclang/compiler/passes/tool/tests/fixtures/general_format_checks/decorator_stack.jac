can star(func: Any) {
    can inner(x: Any) {
        print(("*" * 30));
        func(x);
        print(("*" * 30));
    }
    return inner;
}

can percent(func: Any) {
    can inner(y: Any) {
        print(("%" * 30));
        func(y);
        print(("%" * 30));
    }
    return inner;
}

can percent2(func: Any) {
    can inner(y: Any) {
        print(("-" * 30));
        func(y);
        print(("+" * 30));
    }
    return inner;
}

@star
@percent
@percent2
can printer(msg: Any) {
    print(msg);
}

with entry {
    printer("Hello");
}
