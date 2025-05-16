import time;
node A {
    has val: int;

    can do1 with W entry {
        print("A Entry action ", self.val);
        visit [self-->];
        time.sleep(1);
    }
}

async walker W {
    has num: int;
}

with entry {
    root ++> (a1 := A(1)) ++> [a2 := A(2), a3 := A(3), a4 := A(4)];
    w1 := W(8);
    task = w1 spawn a1;
    print("It is non blocking");
    result = await task ;
    print(result);
}
