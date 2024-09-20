node a{
    has vv:int =23;
}


with entry{
    x = a();
    root ++> x;
    print([root -->]);
    del x;
    print([root -->]);

}


node test_node {
    has value: int;
}

with entry {
    root ++> (my_node:=test_node(value=0));
    print(my_node);
    root del--> my_node;
    print(my_node);
}