node test_node {
    has name;
}
edge special;
graph test_graph {
    has anchor graph_root;
    graph G {
        graph_root [node=test_node, name=root]
        node_1 [node=test_node, name=node_1]
        node_2 [node=test_node, name=node_2]
        graph_root -> node_1 [edge=special]
        graph_root -> node_2
    }
}
walker init {
    has nodes;
    with entry {
        nodes = [];
    }
    root {
        spawn here --> graph::test_graph;
        take --> node::test_node;
    }
    test_node {
        nodes += [here];
        take -[special]-> node::test_node;
    }
    report here;
}