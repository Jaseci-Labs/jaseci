# Nodes

Nodes are the building blocks of any JAC program. Nodes are the destinations of Walkers. Nodes have abilities which are similar to functions in python. These abilities can be triggered when walkers traverse on to or leave the Node or even triggered by the Walker if needed. 
Nodes can be created to serve different functions. All Nodes are linked together in a graph by edges.

A node is a representation of an entity.

* Nodes are composed of Context and excetuable actions.
* Nodes accumulate context via a push function, context can be read ass well
* Nodes can execute a set of actions upon entry and exit.

## Defining Node Attributes
Attributes are variables within the node. The `has` keyword is used to declare an attribute within a node. Nodes also have abilities . These abilities can be either be written or be leaveraged from Jaseci_Kit . The `can` keyword is used to declare an ability. 

```jac 
node [name of node]{
    # to declare an attribute we uses the [has] keyword followed by the attribute name.
    has variable;
    # to use a module from jaseci kit
    can use_qa;
    # a written ability
    can talk {
        # code to be executed added here
    }
}
```

## Adding abilities


Functions in JAC are avalibale to Nodes only. They are called Abilities instead of Functions.These abilities can be activated when a walker travers over a node . Abilities can be triggered when a Walker first traverse over a node , leaves a node , triggered by the walker or when a specific walker enter or leaves a node.

Abilities in nodes can be declared as followed:

```jac 
node state {
  # any walker can use ability
  can ability6 {
    # execute some code
  }
  # Walker enters a node 
    can ability  entry {
        #execute some code.
    }
    # Walker exits a node 
    can ability2  exit {
        # execute some code 
    }
    
    # specific walker enters
    can ability3 with walker1 entry {
        # execute some code
    }

    # specific walker exits
    can ability4 walker1 exits {

    }

    # only specifc walker can use ability 
    can ability5 walker2 {
        # code to execute
    }
}

```

## Inheritance on Nodes 

Nodes can inherit abilities and attributes of other nodes. 

```jac
# parent node 

node state {
    has title;
    has message;
    has prompts;
}

# inherits attributes from state node.
node input_state:state {
    has input;
}

# inherits attributes from input_state.
node output_state :input:state{
    has output;
}
```