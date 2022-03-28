dot_node = \
    """
    node test_node {has name;}
    graph test_graph {
        has anchor graph_root;
        graph G {
            graph_root [node=test_node, name=graph_root_node_name];
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
            graph_root [node=test_node, name=graph_root_node_name];
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

dot_node_multi_stmts = \
    """
    node test_node {
        has name, date;
    }
    graph test_graph {
        has anchor graph_root;
        graph G {
            graph_root [node=test_node]
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
            graph_root [node=test_node, name=root]
            node_1 [node=test_node, name=node_1]
            node_2 [node=test_node, name=node_2]
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
        with exit {
            for i in nodes {
                std.out(i.name);
            }
        }
    }
    """

dot_edge_with_attrs_vars = \
    """
    node test_node {
        has name;
    }
    edge special {
        has name;
    }
    graph test_graph {
        has anchor graph_root;
        graph G {
            graph_root [node=test_node, name=root]
            node_1 [node=test_node, name=node_1]
            node_2 [node=test_node, name=node_2]
            graph_root -> node_1 [edge=special, name=edge_1]
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
            for i in -[special]->.edge {
                std.out(i.name);
            }
            for i in -[special(name == "edge_1")]-> {
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
    graph test_graph {
        has anchor A;
        strict graph G {
            H [node=year]
            C [node=week]
            E [node=day]
            D [node=day]

            A -> B // Basic directional edge
            B -- H // Basic non-directional edge
            B -> C [edge=parent] // Edge with attribute
            C -> D -> E [edge=child] // Chain edge

            A [color=red] // Node with DOT builtin graphing attr
            B [node=month, count=2] [season=spring]// Node with Jac attr
            A [node=year] // Multiple attr statement per node
        }
    }
    walker init {
        root {
            spawn here --> graph::test_graph;
        }
    }
    """

dot_quoted_string = \
    """
    node test_node {
        has name;
    }
    graph test_graph {
        has anchor graph_root;
        graph G {
            graph_root [node=test_node, name=root]
            node_1 [node=test_node, name="this has space"]
            node_2 [node=test_node, name="another space"]
            graph_root -> node_1
            graph_root -> node_2
        }
    }
    walker init {
        root {
            spawn here --> graph::test_graph;
        }
        test_node {
            report here.name;
        }
        take -->;
    }
    """
