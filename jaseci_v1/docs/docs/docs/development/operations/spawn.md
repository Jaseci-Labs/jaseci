---
sidebar_position: 1
title: Spawn
---

The `spawn` keyword has various applications in graphs, nodes, and walkers, each with its own unique context. To gain a better understanding of its usage in each of these contexts, please refer to the following sections.

## Graph Spawn

In the `graph`s , the spawn keyword is utilized to generate or create graphs.

```jac
node product {
    has name;
    has stock = 0;

}

edge category {
    has name;
}

# Initial graph for the shop
graph shop {
    has anchor catalog;
    spawn {
        catalog = spawn node::product_catalog;

        apple = spawn node::product(name="apple");
        catalog +[category(name="fruit")]+> apple;

        banana = spawn node::product(name="banana");
        catalog +[category(name="fruit")]+> banana;

        notebook = spawn node::product(name="notebook");
        catalog +[category(name="supplies")]+> notebook;
    }
}

```

## Node Spawn

To create a child node from a parent node, the `spawn` keyword is used in `node`s.

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
```

## Walker Spawn

To initiate traversing a walker from a node the `spawn` keyword is used in `walker`s.

```jac
walker init {
    root {
        spawn here walker::build_example;
    }
    }
```

Or to initiate a `graph` from a root `node` as following;

```jac
walker init {
    root: spawn here ++> graph::shop;
}
```