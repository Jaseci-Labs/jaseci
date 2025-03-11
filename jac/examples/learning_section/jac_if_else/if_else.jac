"""Python Conditions and If statements"""

with entry{
    a=5;
    b=20;
    if b>a {
        print("b is greater than a");
    }
}

"""Elif"""
with entry{
    a=5;
    b=20;
    if b>a {
        print("b is greater than a");
    } elif a==b {
        print("a and b are equal");
    }
}

"""Else"""
with entry{
    a=5;
    b=20;
    if b>a {
        print("b is greater than a");
    } elif a==b {
        print("a and b are equal");
    } else {
        print("a is greater than b");
    }
}

"""Short Hand If"""
with entry{
    if a>b { print("a is greater than b");}
}

"""And"""
with entry{
    a=5;
    b=20;
    c=100;
    if a>b and c>a{
        print("Both conditions are True");
    }
}

"""Or"""
with entry{
    a=5;
    b=20;
    c=100;
    if a>b or c>a{
        print("At least one of the conditions is True");
    }
}

"""Not"""
with entry{
    a=5;
    b=20;
    if not a>b {
        print("a is NOT greater than b");
    }
}

"""Nested if"""
with entry{
    x=50;
    if x>10{
        print("Above ten,");
        if x>20{
            print("and also above 20!");
        } else{
            print("but not above 20.");
        }
    }
}