edge back;

walker init {
    node_a = spawn node;
    here --> node_a;
    here <-[back]- node_a;

    node_b = spawn here <-> node;
    node_b --> node_a
}