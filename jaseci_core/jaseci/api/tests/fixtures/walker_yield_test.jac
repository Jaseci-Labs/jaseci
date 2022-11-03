node A;
node B;

graph G {
    has anchor a;
    spawn {
        a = spawn node::A;
        b = spawn node::B;
        a --> b;
    }
}
walker W {
    root: take -->;
    A {
        take --> node::B;
        report "I am yielded now. Going to B next";
        yield;
    }
    B {
        report "I am at B. Bye";

    }
}

test "Delete yielded walker in test"
with graph::G by walker::W {
    std.out(std.get_report());
}

test "Delete yielded walker in test 2"
with graph::G by walker::W {
    std.out(std.get_report());
}

