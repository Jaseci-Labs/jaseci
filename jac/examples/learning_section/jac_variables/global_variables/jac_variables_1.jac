with entry {
    x = "awesome";
    can myfunc() {
        print("Jaclang is " + x);
    }
    myfunc();
}

with entry {
    x = "awesome";
    can myfunc() {
        x = "fantastic";
        print("Jaclang is " + x);
    }
    myfunc();

    print("Jaclang is " + x);
}

glob x = "awesome";

with entry {
    can myfunc() {
        print("Jaclang is " + x);
    }
    myfunc();
}

glob x = "awesome";

with entry {
    can myfunc() {
        x = "fantastic";
        print("Jaclang is " + x);
    }
    myfunc();

    print("Jaclang is " + x);
}
