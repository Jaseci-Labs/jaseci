node simple: has name;
edge conn: has name="points_to";

walker has_var_plucking {
    with entry {
        for i=0 to i<3 by i+=1: spawn here -[conn]-> node::simple(name="test");
    }
    report -->.edge.name;
}