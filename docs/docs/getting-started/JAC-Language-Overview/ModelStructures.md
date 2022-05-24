---
title: Modelling Strucutres with Nodes,Edges and Graphs
---


Nodes , Edges and Graphs are vital to any Jaseci program. 

### Nodes
A node is a representation of an entity.

* Nodes are composed of Context and excetuable actions.
* Nodes accumulate context via a push function, context can be read ass well
* Nodes can execute a set of actions upon entry and exit.

```jac 
node [name of node]{
    # to declare a variable
    has variable;
    # to use a module from jaseci kit
    can use_qa;
}
```

### Edges
* can be thought of as a relationship between nodes.
* Edges accumulate context via a push function , context can be read as well.
* Edges execute a set of actions when traversed.

```jac
edge [name of edge] {
    has variable;
}
```

### Graphs
* can be thought as the collections of nodes
* Within the Graph is where we link nodes and edges together to create conversational flows.

```jac
graph [name of graph] {
    this is the root node of the graph
    has anchor [name of anchor];

    #here is where we start to connect nodes with edges creating a graph.
    spawn{
        # declare your nodes in here 

     }
}
```