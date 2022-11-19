node simple: has name;

walker ref_deref {
    with entry {
        for i=0 to i<3 by i+=1:
            spawn here ++> node::simple(name="node"+i.str);
    }
    var = &(-->[0]);
    std.out('ref:', var);
    std.out('obj:', *var);
    std.out('info:',(*var).info);
}