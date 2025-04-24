with entry {
    a = 5;
    b = 20;
    if b > a {
        print("b is greater than a");
    }
}

with entry {
    a = 5;
    b = 20;
    if b > a {
        print("b is greater than a");
    } elif a == b {
        print("a and b are equal");
    }
}

with entry {
    a = 5;
    b = 20;
    if b > a {
        print("b is greater than a");
    } elif a == b {
        print("a and b are equal");
    } else {
        print("a is greater than b");
    }
}

with entry {
    a = 5;
    b = 20;
    c = 100;
    if a > b and c > a {
        print("Both conditions are True");
    }
}

with entry {
    a = 5;
    b = 20;
    c = 100;
    if a > b or c > a {
        print("At least one of the conditions is True");
    }
}

with entry {
    a = 5;
    b = 20;
    if not a > b {
        print("a is NOT greater than b");
    }
}

with entry {
    x = 50;
    if x > 10 {
        print("Above ten,");
        if x > 20 {
            print("and also above 20!");
        } else {
            print("but not above 20.");
        }
    }
}
