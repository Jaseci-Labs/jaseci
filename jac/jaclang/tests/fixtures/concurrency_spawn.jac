import:py from time { sleep }
node A{
    has val: int;

    can do1 with W entry {
        print("A Entry action ", self);
        visit [self -->];
    }
    can do2 with W exit {
        print("A Exit action ", self);
    }
}

walker W{
    has num: int;

    can do1 with entry {
        print("W Entry action ", here);
    }
    can do2 with exit {
        print("W Exit action ", here);
    }
}

with entry {
    root ++> (a1:=A(1)) ++> [a2:=A(2), a3:=A(3), a4:=A(4)];
    [a2,a3] ++> (a5:=A(5));
    [a4,a5] ++> (a6:=A(6));
    w2 = (w1 := W(8)) jacgo spawn a1;
    print("Walker W spawn action", w2);

}