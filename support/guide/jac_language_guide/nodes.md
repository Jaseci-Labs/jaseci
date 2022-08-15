# Nodes

A node is a representation of an entity.

* Nodes are composed of Context and excetuable actions.
* Nodes accumulate context via a push function, context can be read ass well
* Nodes can execute a set of actions upon entry and exit.

```jac 
node [name of node]{
    # to declare a variable
    has variable;
    # to use a module from jaseci kit
    can use_qa;
}
```