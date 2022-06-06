---
title : Multiple Inheritance 
---
JAC allows for multiple inheritance.

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