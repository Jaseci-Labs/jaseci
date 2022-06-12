---
title : Multiple Inheritance 
---
JAC allows for nodes and edges  to inherit attributes and functions of the same type .

### Node Inheritance
```jac
node state {
    has title;
    has message;
    has prompts;
}

node input_state:state {
    has input;
}

node output_state :input:state{
    has output;
}
```

### Edge Inheritance

```jac 
edge transition {
    has transition_next ;
}

edge transition_back: transition {
    has prev_step ;
}
```
