---
title: Operating Context
---
# Specifying Operating Context

Several types Of  Nodes can be created and each can  have several unique abilities. The abilities of specific nodes can be activated when a walkers traverese on to it . This can be done by specifying an operating context. This allows a walker to execute any of the nodes ability that it is currently on. The operating context of each type of node must be specified for it to be used.

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