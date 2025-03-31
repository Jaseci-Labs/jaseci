"""Jac variable Introduction"""

with entry {
    x:int = 5;
    y:str = "Tom";
    print(x);
    print(y);
}

with entry {
    x = str(3);
    y = int(3);
    z = float(3);
    print(x);
    print(y);
    print(z);
}

with entry {
    x:int = 5;
    y:str = "Tom";
    print(type(x));
    print(type(y));
}

with entry {
    a = 4;
    A = "Sally";
    print(a);
    print(A);
}

"""Jac variable Names"""
with entry {
    myvar = "John";
    my_var = "John";
    _my_var = "John";
    myVar = "John";
    MYVAR = "John";
    myvar2 = "John";
}

"""Jac Output variables"""
with entry {
    x = "Jaclang is awesome";
    print(x);
}

with entry {
    x = "Jaclang";
    y = "is";
    z = "awesome";
    print(x, y, z);
}

"""Jac Global variable"""
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
