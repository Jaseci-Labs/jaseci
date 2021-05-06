dot_node = \
    """
    node test_node {has name;}
    graph test_graph {
        has anchor graph_root;
        graph G {
            graph_root [kind=test_node, name=graph_root_node_name];
        }
    }
    walker init {
        root {
            spawn here --> graph::test_graph;
            take --> node::test_node;
        }
        test_node {
            std.out(here.name);
        }
    }
    """

dot_node_no_dot_id = \
    """
    node test_node {has name;}
    graph test_graph {
        has anchor graph_root;
        graph {
            graph_root [kind=test_node, name=graph_root_node_name];
        }
    }
    walker init {
        root {
            spawn here --> graph::test_graph;
            take --> node::test_node;
        }
        test_node {
            std.out(here.name);
        }
    }
    """

spawn_graph_node = \
    """
    node test_node {has name;}
    graph test_graph {
        has anchor graph_root;
        spawn {
            graph_root = 
                spawn node::test_node(name="graph_root_node_name");
        }
    }
    walker init {
        root {
            spawn here --> graph::test_graph;
            take --> node::test_node;
        }
        test_node {
            std.out(here.name);
        }
    }
    """

dot_node_overwrite_name = \
    """
    node test_node {has name;}
    node subnode;
    graph test_graph {
        has anchor graph_root;
        graph G {
            graph_root [kind=test_node, name=graph_root_node_name]
            placeholder [_n_name_=real_name, kind=subnode]
            graph_root -> placeholder
        }
    }
    walker init {
        root, test_node {
            spawn here --> graph::test_graph;
            take -->;
        }
        subnode {
            std.out(here);
            disengage;
        }
    }
    """


dot_node_multi_stmts = \
    """
    node test_node {
        has name, date;
    }
    graph test_graph {
        has anchor graph_root;
        graph G {
            graph_root [kind=test_node]
            graph_root [name=test_node, date=2021]
            graph_root [name=real_test_node]
        }
    }
    walker init {
        root {
            spawn here --> graph::test_graph;
            take --> node::test_node;
        }
        test_node {
            std.out(here.name);
            std.out(here.date);
        }
    }
    """

dot_edge = \
    """
    node test_node {
        has name;
    }
    graph test_graph {
        has anchor graph_root;
        graph G {
            graph_root [kind=test_node, name=root]
            node_1 [kind=test_node, name=node_1]
            node_2 [kind=test_node, name=node_2]
            graph_root -> node_1
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
            take --> node::test_node;
        }
        with exit {
            for i in nodes {
                std.out(i.name);
            }
        }
    }
    """

dot_edge_with_attrs = \
    """
    node test_node {
        has name;
    }
    edge special;
    graph test_graph {
        has anchor graph_root;
        graph G {
            graph_root [kind=test_node, name=root]
            node_1 [kind=test_node, name=node_1]
            node_2 [kind=test_node, name=node_2]
            graph_root -> node_1 [kind=special]
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
        with exit {
            for i in nodes {
                std.out(i.name);
            }
        }
    }
    """

dot_graph = \
    """
    node year {
        has color;
    }
    node month {
        has count, season;
    }
    node week;
    node day;
    edge parent;
    edge child;
    graph test {
        has anchor A;
        strict graph G {
            H [kind=year]
            C [kind=week]
            E [kind=day]
            D [kind=day]

            A -> B // Basic directional edge
            B -- H // Basic non-directional edge
            B -> C [kind=parent] // Edge with attribute
            C -> D -> E [kind=child] // Chain edge

            A [color=red] // Node with DOT builtin graphing attr
            B [kind=month, count=2] [season=spring]// Node with Jac attr
            A [kind=year] // Multiple attr statement per node
        }
    }
    walker init {
        root {
            spawn here --> graph::test;
        }
    }
    """
