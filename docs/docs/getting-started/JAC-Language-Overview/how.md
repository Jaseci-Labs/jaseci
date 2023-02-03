---
title: How a JAC program runs
---

The JAC Promgrammming language builds its paradigm on the traversal of Graphs. Graphs comprises of nodes and edges . Nodes have abilities that can be activated when a walker travers on it. The Walker traverse the graph and decides which paths to take by using the edges.

All traversal begins at the Init or default node. This `init` node will connect to the main root of our graph.


![Pic of Main Root](/img/tutorial/intermediate/root.png)

The Walkers are initialized and added on the root node and from there they begin traveral.
The walkers decide which node to travel to based on which edge satisfies it's intent. The intent being a criteria meet by the edge.

![Pic of Nodes and Edges](/img/tutorial/intermediate/graph.png)

The Walker can move from node to node along edges. It can also be spawned directly on any node without the need for a traversal
