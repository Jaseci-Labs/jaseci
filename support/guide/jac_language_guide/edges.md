# Edges

Edges are the links that connect nodes to each other

* Edges associate one node with another by way of a uni-directional or bidirectional path definition.
* Edges are composed of context and executable actions.
* Edges accumulate context via a push function, context can be read as well.
* Edges execute a set of actions when traversed.
* Edges much be aware of the set of HDGDs of which it is a member.
* Edges crossing HDGD boundaries must trigger higher order HDGD plane edges.


```jac 
edge [name of edge] {
    has variable;
}

```