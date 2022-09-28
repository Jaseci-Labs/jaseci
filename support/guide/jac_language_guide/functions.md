# Functions

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