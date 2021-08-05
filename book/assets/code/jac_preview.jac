node simple;
edge back;

walker init {
    node_a = spawn here --> node::simple;
    here <-[back]- node_a;

    node_b = spawn here <--> node::simple;
    node_b --> node_a;
}