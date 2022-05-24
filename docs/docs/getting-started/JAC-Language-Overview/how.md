---
title: How a JAC program runs
---

The JAC Promgrammming language builds its paradigm on traversal of Graphs. The Walker is used to traverse graphs . The graph is a combination of nodes and edges connected together. We create our graphs and walkers and specify their abilities.

All traversal begins at the Init or default node. This `init` node will connect to the main root of our graph.


![Pic of Main Root](/img/tutorial/intermediate/root.png)

The Walkers are initialized and added on the root node and from there they begin traveral.
The walkers decide which node to travel to based on which edge satisfies it's intent. The intent being a criteria meet by the edge.

![Pic of Nodes and Edges](/img/tutorial/intermediate/graph.png) 

The Walker can move from node to node but it can also jump to other nodes that are not in it's path or connected directly in the path.
