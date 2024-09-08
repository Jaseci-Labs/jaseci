walker init {
    node1 = spawn node::generic;
    node2 = spawn node::generic;
    node1 <--> node2;
    here --> node1;
    node2 <-- here;
}