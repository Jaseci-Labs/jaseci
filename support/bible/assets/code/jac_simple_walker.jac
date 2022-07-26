node plain;

walker init {
    node1 = spawn node::plain;
    node2 = spawn node::plain;
    node1 <--> node2;
    here --> node1;
    node2 <-- here;
}