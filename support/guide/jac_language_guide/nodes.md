# Nodes

Nodes are the building blocks of any JAC program. Nodes are the destinations of Walkers. Nodes have abilities which are similar to functions in python. These abilities can be triggered when walkers traverse on to or leave the Node or even triggered by the Walker if needed. 
Nodes can be created to serve different functions. All Nodes are linked together in a graph by edges.

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