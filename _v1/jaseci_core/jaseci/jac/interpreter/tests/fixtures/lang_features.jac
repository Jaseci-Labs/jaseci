node simple: has name;
edge conn: has name;

walker has_var_plucking {
    with entry {
        for i=0 to i<3 by i+=1:
            spawn here +[conn(name="edge"+i.str)]+>  node::simple(name="node"+i.str);
    }
    report -->.name;
    report -->.edge.name;
}

walker deref_adaptive {
    with entry {
        for i=0 to i<3 by i+=1:
            spawn here +[conn(name="edge"+i.str)]+>  node::simple(name="node"+i.str);
    }
    var = &(-->[0]);
    var = "junk and stuff"+var.s::lstrip("urn:uuid:");
    report var;
    report (*var).context;
}

walker deref_of_element_fails {
    with entry {
        for i=0 to i<3 by i+=1:
            spawn here +[conn(name="edge"+i.str)]+>  node::simple(name="node"+i.str);
    }
    var = (-->[0]);
    report (*var).context;
}

walker quick_check {
    a = spawn here +[conn(name="edge"+"5")]+> node::simple;
    report a.edge[0].name;
}