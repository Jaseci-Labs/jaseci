# Key Language Level Abstractions and Concepts

There are a number of abstractions and concepts in Jac that is distinct from most (all?) other languages. These would be a good place to begin understanding for a seasoned / semi-seasoned programmer. In a nutshell...

## Graphs
The graph is a key and first order data abstraction used in Jaseci/Jac. A foremost Jaseci priciple is that almost every computational problem can be mapped into a graph structure and can be solved by traversing and executing nodes in the graph, and graphs are a rich and intuitive semantic to use when reasoning about problems.

## Walkers
A walker is an execution unit that moves(traverses) through a graph while preserving its state (its local scope). This semantic is novel to traditional programming languages. You can imagine a walker as a little, self-contained robot that can maintain context while it moves spatially around a graph, interacting with the context (scope) within its nodes and edges.

## Abilities
Nodes, edges, and even walkers in the graph can have abilities (computational routines tethered to the object). Though they don’t have the same semantics as a typical function/method. Abilities are most nearly comparable to methods in traditional object-oriented programming, though these routines can only see the data in the walker and the node and edge it sits on. You can imagine abilities as independent in-memory/in-data computing activities when employing them.

## Actions
Actions share the semantics as traditional function calls with returns, however these primarily serve to enable bindings to the functionality described outside of Jac/Jaseci (ie in a python module). These are comparable to library calls in conventional programming languages. Actions are essentially bindings to external functionality takes the form of a Jaseci action library’s direct connection to Python implementations.