node testnode {
    has yo, bro;
}

node apple {
    has v1, v2;
}

node banana {
    has x1, x2;
}

graph dummy {
    has anchor graph_root;
    spawn {
        graph_root = spawn node::testnode (yo="Hey yo!");
        n1=spawn node::apple(v1="I'm apple");
        n2=spawn node::banana(x1="I'm banana");
        graph_root --> n1 --> n2;
    }
}

walker init {
    has num=4;
    report here.context;
    report num;
    take -->;
}

test "assert should be valid"
with graph::dummy by walker::init {
    assert (num==4);
    assert (here.x1=="I'm banana");
    assert <--[0].v1=="I'm apple";
}

test "assert should fail"
with graph::dummy by walker::init {
    assert (num==4);
    assert (here.x1=="I'm banana");
    assert <--[0].v1=="I'm Apple";
}

test "assert should fail, add internal except"
with graph::dummy by walker::init {
    assert (num==4);
    assert (here.x1=="I'm banana");
    assert <--[10].v1=="I'm apple";
}