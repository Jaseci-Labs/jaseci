node A {
    has val: int;

    can do1 with W entry {
        print("A Entry action ", self.val);
        jacgo visit [self-->];
    }

    can do2 with W exit {
        print("A Exit action ", self.val);
        here.num = self.val;
    }
}

walker W {
    has num: int;
}

with entry {
    root ++> (a1 := A(1)) ++> [a2 := A(2), a3 := A(3), a4 := A(4)];
    [a2, a3] ++> (a5 := A(5));
    [a4, a5] ++> (a6 := A(6));
    waitgroup([[a5, 2], [a6, 3]]);
    (w1 := W(8)) spawn a1;
}
