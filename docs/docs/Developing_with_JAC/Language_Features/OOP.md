---
title : Multiple Inheritance 
---
JAC allows for objects to inherit attributes and functions or other objects of the same type.

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

### Walker Inheritance

```jac 
walker employee {
    has name;
    has age;
    has position;
}

walker manager : employee { 
    has branch;
    has amount_employees ;
}

walker ass_manager : manager {
    has sub_division ;
}
```