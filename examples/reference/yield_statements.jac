can myFunc() {
    yield "Hello";
    yield 91;
    yield "Good Bye";
}

with entry {
    x = myFunc();
    for z in x {
        print(z);
    }
}
