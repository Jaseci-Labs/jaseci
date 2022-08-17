node simple;
edge back;

walker kewl_graph_creator {
    node_a = spawn here --> node::simple;
    here <-[back]- node_a;
    node_b = spawn here <--> node::simple;
    node_b --> node_a;
}