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
    fam = spawn here walker::friend_ties;
    for i in fam:
        std.out(here, 'is related to\n', i, '\n');
}
