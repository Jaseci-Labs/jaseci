---
title : Multiple Inheritance 
---
Jaseci allows for Entities to perform multiple inheritance.

```jac
node state {
    has title;
    has message;
    has prompts;
}

node input_state:state {
    has input;
}

```