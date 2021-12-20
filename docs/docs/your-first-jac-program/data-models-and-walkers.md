---
sidebar_position: 2
---

# Data models and walkers

Here we'll look at setting up the Jaseci data model (nodes and edges) and defining the walkers to support the feature list.

>  **From the Docs**

> - **Nodes** represent an entity on a graph. [Learn more](/docs/intermediate/standard-library-documentation/jaseci-primitives#node)
> - **Edges** represent the relationship between nodes on a graph. [Learn more](/docs/intermediate/standard-library-documentation/jaseci-primitives#edge)
> -  **Walkers** traverse nodes via edges executing logic at the node level. [Learn more](/docs/intermediate/standard-library-documentation/jaseci-primitives#walker)

## Data Model

`person` node

Members of the network are defined as `person` nodes with one attribute, `name`. For simplicity, we will also assume that each `person` has a unique `name`. This allows us to use `name` as the anchor for the node to make handling this type of node easier (as in comparisons, for example).

```
// person node to represent members of the network
node person {
    has anchor name;
}
```

<!-- TODO: Update the below links -->
>  **From the Docs**
> - **has** defines a property on a node or walker. [Learn more](/docs/intermediate/standard-library-documentation/built-in-operations#has)
> - **anchor** defines the primitive representation or return value of a node or walker. [Learn more](/docs/intermediate/standard-library-documentation/built-in-operations#anchor)

`friend` edge

We will use a named undirected edge called `friend` to describe the relationship between `person` nodes on the network.

```
// friend edge to describe the relationship between person nodes
edge friend;
```

## Walkers

### Joining the network

This walker is intended to be run on the `root` node. It creates a `person` node connected to `root` by an unnamed undirected edge. It has a `name` attribute which is passed through to the `person` being created.

```
walker join {
    has name;

    root {
        report spawn here <--> node::person(name=name);
    }
}
```

<!-- TODO: Update the below links -->
>  **From the Docs**
> - **root** is a built-in node that represents the starting point of a graph.
> - **spawn** creates a node with or without edges or runs a walker on a node. [Learn more](/docs/intermediate/standard-library-documentation/built-in-operations#spawn)

### Listing members of the network

This walker is intended to be run on the `root` node. It walks the graph returning a list of `person` nodes that represents all network members.

```
// gets all members of the network
walker get_members {
    has anchor members;

    with entry {
        members = [];
    }

    root {
        take -->;
    }

    person {
        members += [here];
    }
}
```

<!-- TODO: Update the below links -->
>  **From the Docs**
> - **with entry / exit** defines a block of code to execute when a walker first enters or is about the exit a node. **with entry** can be used to initialize the walker's attributes, while **with** exit can be used to report a return value as a walker completes execution. [Learn more](/docs/intermediate/standard-library-documentation/jaseci-primitives#with-entry--with-exit)

## Adding friends

This walker is intended to be run on a `person` node. It creates an undirected `friend` edge between the node on which it is run and another `person` node defined by the `new_friend` attribute.

```
// adds a friend to the person node being walked
walker add_friend {
    has new_friend;

    person {
        here <-[friend]-> new_friend;
    }
}
```

## Getting friend list

This walker is intended to be run on a `person` node. It gets a list of `person` nodes that are connected to the node on which it is run by an undirected `friend` edge. This represents that person's friend list.

```
// get the list of friends of the person node being walked
walker get_friend_list {
    has anchor friend_list;

    with entry {
        friend_list = [];
    }

    person {
        friend_list += <-[friend]->;
    }

    with exit {
        for friend in friend_list {
            report friend;
        }
    }
}
```

## Getting suggested friends

This walker is intended to be run on a `person` node. It gets a list of `person` nodes that are suggested friends for the node on which it is run.

The current algorithm suggests friends of existing friends, i.e. persons with whom there is a mutual friend.

**Note**: There is a bug where it might suggest friends that you already have. Who can find and/or fix it? ;-)

```
// gets suggested friends for the person node being walked
// current algorithm: suggest friends of friends (mutual friends)
walker get_suggested_friends {
    has anchor suggestions;

    with entry {
        suggestions = [];
    }

    person {
        for f in <-[friend]-> {
            for sug in spawn f walker::get_friend_list() {
                if sug != here {
                    suggestions += [sug];
                    report sug;
                }
            }
        }
    }
}
```

On to [Building the application!](/docs/your-first-jac-program/build-the-jac-code-and-application)
