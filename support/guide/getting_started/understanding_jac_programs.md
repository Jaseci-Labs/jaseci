# Understanding JAC Programs

JAC Programs are authored by the JAC language which is used to define structure and behaviour. Behaviour can be modeled in the form of actions and abilities within node elements of the graph as well as walker elements which are specifically designed to traverse the nodes and edges of a graph. Structure can be modeled by arranging a number of nodes and edges in a particular manner, compelte with state, to form a graph. 

When a JAC program executes, the structural and behavioral definitions encoded in JAC are registered with the Jaseci Runtime Machine in the form of a Sentinel. Named Walkers may then be launched on a graph via an API call. 

Walkers may be designed to report their output. Reports come back via API once a walker has completed its walk, these reports will be a json payload of objects.

Graphs comprise nodes and edges. Nodes have abilities that can be activated when a walker travers on it. The Walker traverse the graph and decides which paths to take by using the edges. 

All traversal begins at the Init or default node. This `init` node will connect to the main root of our graph.

![Pic of Main Root](../assets/root_node.png)

The Walkers are initialized and added on the root node and from there they begin traveral.
The walkers decide which node to travel to based on which edge satisfies it's intent. The intent being a criteria meet by the edge.

![Pic of Nodes and Edges](../assets/graph.png) 

The Walker can move from node to node along edges. It can also be spawned directly on any node without the need for a traversal