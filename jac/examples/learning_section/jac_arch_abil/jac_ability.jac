can say_hello {
    print("Hello!");
}

can say_hello_to(name: str) {
    print("Hello, " + name + "!");
}

can add(a: int, b: int) -> int {
    return a + b;
}

obj Maths {
    static can square(n: int) -> int {
        return n * n;
    }
}