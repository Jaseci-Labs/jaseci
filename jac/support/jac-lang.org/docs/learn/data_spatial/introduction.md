# Graphs

It's interesting to see how much programming languages have progressed over the years. However, one essential data structure, graphs, has not received much attention. **Almost every data structure used by programmers, such as stacks, lists, queues, trees, and heaps, can be described as a type of graph, except for hash tables**. Despite this, no programming language has welcomed graphs as its primary data representation.

Graphs are easy for humans to understand, which makes them great for solving computational problems, especially in fields like AI. Some people say that current graph libraries in their favorite programming languages are good enough, so there's no need for a language focused on graphs. However, programming languages are based on their main ideas, and since graphs aren't a fundamental part of these languages, they are not designed for the detailed meanings that graphs offer.

One concern is that if graphs become the main way data is organized, it could make the language slower. However, many modern languages already use complex ways of organizing data, like dynamic typing, which can slow down the program when it runs. Jaclang wants to change how we think about data and memory by using graphs as the foundation for memory representation, because they naturally have a lot of meaning and information.

We make follwoing assumptions about graphs in jaclang:

1. **Directed Graphs with Flexible Edges**: Graphs are directed, meaning edges have a specific direction from one node to another.
There’s a special type of edge that points both ways,
allowing it to act like an undirected edge if needed.
2. **Unique Identity for Nodes and Edges**: Both nodes and edges have their own unique identities, so an edge isn’t just a simple connection between two nodes. This is important because both nodes and edges can store additional information or context.
3. **Multigraphs and Self-Loops**: Multiple edges between the same pair of nodes are allowed, as well as edges that start and end on the same node (self-loops).
4. **No Requirement for Acyclic Structure**: Graphs don’t have to be acyclic, meaning cycles (paths that loop back to the starting node) are allowed.
5. **No Hypergraphs**: Hypergraphs (where an edge can connect more than two nodes) are not supported to keep things simpler for Jaseci programmers.

Refer to [Wikipedia description of graphs](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)) to learn more about graphs.


## Nodes

Nodes are the fundamental units in a graph and can hold both variables and abilities. Variables store specific attributes or data related to the node, while abilities are like functions or methods associated with the node. These abilities can be triggered to perform tasks, such as modifying the node's properties, interacting with other nodes, or carrying out specific actions within the graph. This combination of data and functionality makes nodes both informative and interactive.

There are two types of nodes:

- **Root node**: It is the starting point of the graph and is a built-in node type. Each graph can have only one root node.
- **Generic node**: It is a built-in node type that can be used throughout the program. You can customize the name and properties of this node type.

Here's an example code snippet to create a generic node:

```jac
node student{
    has name: str;, age:int;
}

node subject{
    has name: str = "programming";
}
```

In jaclang, variables within a node are defined with the `has` keyword. We can also set default values for these variables, as demonstrated in the `subject` node.

## Edges

Edges are an essential component of the graph structure, and they allow for more complex relationships between nodes. As stated above, just like nodes, you can define custom edge types with variables, and abilities.

Here is a example of creating a edge.

```jac
edge attend{
    has hours = 2;
}
```

## Connect Nodes and Edges


```jac

```

## Display graph

## Traversing in graph

### Walkers
### Visit
### Delete nodes
### Delete edges
