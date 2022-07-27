node person;
edge friend;
edge family;

walker init {
    node1 = spawn node::person;
    node2 = spawn node::person;
    node2 <-[friend]- here -[friend]-> node1 <-[family]-> node2;
}