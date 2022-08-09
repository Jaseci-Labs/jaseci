node simple: has name;
edge conn: has name;

walker has_var_plucking {
    with entry {
        for i=0 to i<3 by i+=1:
            spawn here -[conn(name="edge"+i.str)]-> node::simple(name="node"+i.str);
    }
    report -->.name;
    report -->.edge.name;
}