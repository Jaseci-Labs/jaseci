node person;
edge friend;
edge family;

walker friend_ties {
    has anchor fam_nodes;
    fam_nodes = -[friend]->;
}

walker init {
    node1 = spawn here -[friend]-> node::person;
    node2 = spawn node1 <-[family]-> node::person;
    here -[friend]-> node2;
    for i in spawn here walker::friend_ties:
        std.out(here, 'is related to\n', i, '\n');
}