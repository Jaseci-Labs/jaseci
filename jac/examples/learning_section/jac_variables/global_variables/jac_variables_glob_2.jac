glob x = "awesome";

with entry {
    can myfunc() {
        x = "fantastic";
        print("Jaclang is " + x);
    }
    myfunc();

    print("Jaclang is " + x);
}
