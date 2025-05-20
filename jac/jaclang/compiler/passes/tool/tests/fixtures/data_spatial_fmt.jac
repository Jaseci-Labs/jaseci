node MyNode {}


with entry {
    first_tier = [MyNode() for i in range(2)];
    second_tier = [MyNode() for i in range(2)];
    root ++> first_tier;
    first_tier ++> second_tier;
    end_tier = MyNode();
    second_tier ++> end_tier;
}


with entry {
    first_tier = [MyNode() for i in range(2)];
}


node A {
    has val: int = 0;
}


node B {
    has val: int = 0;
}


node C {
    has val: int = 0;
}


edge a {}


edge b {}


edge c {}


with entry {
    Start = A(5);
    Intermediate = B(10);
    End = C(25);
    root +>:a:+> Start;
    Start +>:b:+> Intermediate +>:c:+> C(15);
    Start +>:b:+> A(20) +>:a:+> End;
    Intermediate +>:c:+> End;
    print([root--> ->:b:->(`?A)]);
    print([root->:a:-> ->:b:-> ->:a:->(`?C)]);
    print([root->:a:-> ->:b:-> ->:c:->(`?C)]);
    print([root->:a:-> ->:b:-> ->:c:->(?val == 25)]);
    print([root->:a:-> ->:b:-> ->:c:->(?val < 20)]);
}


glob x = "Jaclang ";


impl Profile.follow {
    current_profile = [root-->(`?Profile)];
    current_profile[0] +>:Follow():+> self;
    report self;
}


def outer_func-> None {
    :g:x;
    x = 'Jaclang is ';
    y = 'Awesome';
    def inner_func-> tuple[str, str] {
        :nl: y;
        y = "Fantastic";
        return (x, y);
    }
    print(x, y);
    print(inner_func());
}


with entry {
    outer_func();
}


def foo(value: int) {
    assert value > 0 , "Value must be positive";
}


with entry {
    try {
        foo(-5);
    } except AssertionError as e {
        print("Asserted:", e);
    }
    
}


with entry {
    root ++> (a := A());
    ae = [edge root-->a][0];
    Walk(id=1) spawn ae;
    ae spawn Walk(id=2);
}
