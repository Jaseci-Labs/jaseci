---
title: Operating Context
---
# Specifying Operating Context


The Graph can several types of nodes and these nodes can have their own unique abilities.Walkers can be written to perform specific actions when it on a specific node. Call functions or attributes for the node it is on top.
```jac
node state {
    has title;
    has message;
    has prompts;
}

node input_state:state {
    has input;
}

node closing_state:state;

edge transition {
    has intent;
}

walker talker {

state, input_state{

    #execute code specific to the state and input_state nodes

    input_state{

        #These operating context can be embedded within other operating context.
        
    }

}

closing_state{
 
    #execute code specific to  closing_state nodes

}

}

```