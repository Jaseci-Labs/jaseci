node person {
    has age: int;
}

with entry {
    p1 = person(10);
    p2 = person(20);
    p3 = person(30);
    p4 = person(40);

    root ++> p1;
    p1 ++> p2;
    p2 ++> p3;
    p3 ++> p4;

    # before deletion
    a = dotgen(root);
    assert a.count('label=""]') == 4;
    assert a.count('[label="person(') == 4;

    # After delete p2
    del p2;
    # del [p1, p3]; # 1. are we going to support this ?
    b = dotgen(root);
    assert b.count('label') == 3;
    assert '20' not in b;

    # doublecheck p3 also doesnot attach to it
    c = dotgen(p3);
    assert c.count('label="person') == 2;
    assert '20' not in c;

    apple_list = [1, 2, 3, 4, 5];
    del apple_list[2];
    print('apple list after delete 3 :', apple_list);

    del [apple_list[0]];
    # del [apple_list[0], apple_list[1]]; # this will be fixed by the (1) above mentioned
    print('apple list after delete 1 :', apple_list);

    obj Inner {
        has c: list;
        has d: int;
    }
    obj Outer {
        has b: Inner;
    }
    a = Outer(b=Inner(c=[1, 2, 3], d=4));

    print('a.b before delete :', a.b);
    del a.b.c[1];
    print('a.b after delete :', a.b);

}
