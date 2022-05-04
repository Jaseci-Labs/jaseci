node person: has name;

walker get_names {
    std.out(here.name)
    take -->;
}

walker build_example {
    node1 = spawn here --> node::person(name="Joe");
    node2 = spawn node1 --> node::person(name="Susan");
    spawn node2 --> node::person(name="Matt");
}

walker init {
    root {
        spawn here walker::build_example;
        take -->;
    }
    person {
        spawn here walker::get_names;
        disengage;
    }
}