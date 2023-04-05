node testnode {
    has yo, mama;
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
        n1 ++> n2;
        graph_root ++> n2;
    }
}

global hey = "Hey";

walker init {
    has num=4;
    report here.context;
    report num;
    take -->;
}

walker alt_init {
    has num=7;
    report num;
    take -->;
}

test "assert should be valid"
with graph::dummy by walker::init {
    assert (num==4);
    assert (here.x1=="I'm banana");
    assert <--[0].v1=="I'm apple";
}

test the_second
"a second test"
with graph::dummy by walker::init {
    assert (num==4);
    assert (here.x1=="I'm banana");
    assert <--[0].v1!="I'm Apple";
}

test "a third test"
with graph::dummy by walker::init {
    if(num==4): num=5;
    assert (num==5);
    assert (here.x1=="I'm banana");
}
