# Creating Graphs

Now that you know about spawning nodes and viewing information about, you can now leverage that knowledge to create graphs. You create graphs by connecting multiple nodes. This is done using the connect operator ++> <++>. 

```jac
walker init {
    node1 = spawn node::generic;
    node2 = spawn node::generic;
    node1 <++> node2;
    here ++> node1;
    node2 <++ here
}
```

The code shown above generates a graph. You can visualize this graph using Jaseci Studios or the Graphviz graph viewer.

# Statically Creating Graphs

```jac
graph hlp_graph {
 has anchor graph_root;
    spawn {
        graph_root = spawn node::state(name="root_state");
        user_node = spawn node::user;

        state_home_price_inquiry = spawn node::state(name="home_price_inquiry");
        state_prob_of_approval = spawn node::state(name="prob_of_approval");
        graph_root +[user]+> user_node;
        graph_root +[transition(intent_label = "home price inquiry")]+>state_home_price_inquiry;
        graph_root +[transition(intent_label = "robability of loan approval")]+> state_prob_of_approval;
        state_home_price_inquiry +[transition(intent_label = "specifying location")]+> state_home_price_inquiry;
        state_home_price_inquiry +[transition(intent_label = "home price inquiry")]+> state_home_price_inquiry;
        state_home_price_inquiry +[transition(intent_label = "probability of loan approval")]+> state_prob_of_approval;
        state_prob_of_approval +[transition(intent_label = "home price inquiry")]+> state_home_price_inquiry;
    }
}
```

Statically creating graphs means creating a graph that is already fixed and doesn't change. The code above shows an example of how to do that in Jaseci. The graph keyword is used to indicate that a new graph is being created, followed by the name of the graph. The {} are used to wrap everything related to the graph. An anchor named graph_root is declared using the has anchor keyword to identify the starting point of the graph.

After that, the spawn keyword is used to begin the creation of nodes and edges, by using spawn node:: followed by the type of node you want to create (e.g. user or state). You can also specify a name for each node using the name property. Nodes and edges can be connected together using the ++>  operator.

The transition keyword is used to create an edge with a specific intent label. In the example above, the graph has three states: root_state, home_price_inquiry, and prob_of_approval, and a user node. These states and the user node are connected to each other through transitions with intent labels such as "home price inquiry" or "probability of loan approval".

# Semantics of Graphs in Jaseci: Directed Doubly Edged, Multigraphs with Distinct Node and Edge Identities

In Jaseci, we elect to assume the following semantics for the graphs in Jaseci:

1. Graphs are directed with a special case of a doubly directed edge
type which can be utilized practically as an undirected edge.
2. Both nodes and edges have their own distinct identities (i,e. an edge isn’t representable
as a pairing of two nodes). This point is important as both nodes and edges can have
contexts.
3. Multigraphs (i.e., parallel edges) are allowed, including self-loop edges.
4. Graphs are not required to be acyclic.
5. No hypergraphs, as I wouldn’t want Jaseci programmers heads to explode.

Refer to [Wikipedias description of graphs](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)) to learn more about graphs.