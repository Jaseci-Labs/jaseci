node MyNode {
    has value: int = 0;
}

with entry {
    root ++> (x:=MyNode());
    obj_id = jid(x);
    myobj = &obj_id;
    print(obj_id);
    print(myobj);
    print("valid:", myobj == x);


    print(jid(x));
    print(dotgen(x));
}

with entry{
    print(Jac.node_dot(x));
}