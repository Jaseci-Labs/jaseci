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

## Linking Nodes together with an Edge

```jac 

node state {
    has context;
}

edge transition {
    has intent ;
}

graph main {
    has anchor main_root ; 

    # create nodes here with the edges linking them.
    spawn {
        main_root = spawn node:: state(context="main node");

        # create node that connects to main_root
        node_one = spawn main_root -[transition(intent="one")] -> node::state(context="node one");

        
        # connect node that connects to node_one
        node_two  = spawn node_one -[transition(intent="two")] -> node::state(context="node two");

    }

}

```

## Inheritance on Edges

Edges can inherit abilities and attributes of other edges.


```jac
# parent edge 
edge transition {
    has transition_next ;
}
# child edge
edge transition_back:transition {
    has prev_step ;
}
```
