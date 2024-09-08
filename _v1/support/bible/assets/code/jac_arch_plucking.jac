node simple: has n_name;
edge conn: has e_name;

walker node_edge_plucking {
    with entry {
        for i=0 to i<3 by i+=1:
            spawn here -[conn(e_name="edge"+i.str)]-> node::simple(n_name="node"+i.str);
    }
    std.out(-->.n_name);
    std.out(-->.edge.e_name);
}