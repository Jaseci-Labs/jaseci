---
sidebar_position: 1
---

# Spawn

To create a child node from a parent node, the `spawn` keyword is commonly used in Jac Programming language.

Here is an example of `spawn` keyword inside jac program.

```jac
node person: has name;
edge family;
edge friend;

walker build_example {
    spawn here +[friend]+> node::person(name="Joe");
    spawn here +[friend]+> node::person(name="Susan");
    spawn here +[family]+> node::person(name="Matt");
    spawn here +[family]+> node::person(name="Dan");
    }

walker init {
    root {
        spawn here walker::build_example;
        }
}
```
