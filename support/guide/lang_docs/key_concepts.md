# Key Language Level Abstractions and Concepts

There are a number of abstractions and concepts in Jac that is distinct from most (all?) other languages. These would be a good place to begin understanding for a seasoned / semi-seasoned programmer.

## Graphs
The graph is the only data structure used here. Jaseci believes that every computational problem can be mapped into a graph structure and can be solved by traversing and executing nodes in the graph.

## Walkers
A walker is an execution unit that moves(traverses) through a graph while preserving its state (its local scope). There have never been any programming languages with semantics like this one. You can imagine a walker as a little, self-contained robot that can maintain context while it moves spatially around a graph, interacting with the context of its nodes and edges.

## Abilities
Nodes and edges in the graph also the walkers can have abilities. Although they don’t have the same semantics as a typical function, Abilities are most nearly comparable to methods in traditional object-oriented programming. You can imagine abilities as independent in-memory/in-data computing activities when employing them.

## Actions
Actions serve as function calls with returns and enable bindings to the functionality described outside of Jac/Jaseci. These are comparable to library calls in conventional programming languages. In reality, this external functionality takes the form of a Jaseci action library’s direct connection to Python implementations