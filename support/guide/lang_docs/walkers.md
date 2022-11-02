# Walkers

One of the most important abstractions introduced in Jaseci is that of the walker. The
semantics of this abstraction is unlike any that has existed in any programming language
before.

In a nutshell, a walker is a unit of execution that retains state (its local scope) as it travels
over a graphs. Walkers *walk* from node to node in the graph and executing its body.
The walker’s body is specified with an opening and closing braces ( `{` `}` ) and is executed to
completion on each node it lands on. In this sense a walker iterates while spooling through a
sequence of nodes that it ‘takes’ using the take keyword. We call each of these iterations
node-bound iterations.

Variables declared in a walker’s body takes two forms: its context variables, those that
retain state as it travels from node to node in a graph, and its local variables, those that are
reinitialized for each node-bound iterations.

Walkers present a new way of thinking about programmatic execution distinct from the
near-ubiquitous function based asbtraction in other languages. Instead of a functions scope
being temporally pushed onto an ever increasing stack as functions call other functions.
Scopes can be spacially laid out on a graph and walkers can hop around the graph taking its
scope with it. A key difference in this model is in its introduction of data spacial problem
solving. In the former function-based model scopes become unaccessible upon the sub-call of
a function until that function returns. In contrast, walkers can access any scope at any time
in a modular way.

When solving problems with walkers, a developer can think of that walker as a little self-
contained robot or agent that can retain context as it spacially moves about a graph,
interacting with the context in nodes and edges of that graph.

In addition to the introduction of the `take` command to support new types of control flow for node-bound iterations. The keywords and semantics of `disengage`, `skip`, and `ignore` are also introduced. These instruct walkers to stop walking the graph, skip over a node for execution, and ignore certain paths of the graph.

## Basic Walkers Example

When we run a jac code, by default it's exucuting the `init` walker. Basically the `walker init` works as the main method in other programming language. save following code as `main.jac` and run the code in `jsctl` shell with `jac run main.jac`

```
walker init{
    std.out("This is from init walker");
}
```

Output:

```
    jaseci > jac run main.jac
    This is from init walker
```
As you can see, this code has executed the init walker. Now let's create another walker;

```
walker second_walker{
    std.out("This is from second walker \n");
}

walker init{
    std.out("This is from init walker");
    root{
        spawn here walker::second_walker;
    }
}

```

Output:
```
    jaseci > jac run walker_2.jac
    This is from init walker
    This is from second walker
```

The statements from `second walker` and `init` are printed in the jac shell, and we may run just `second_walker` directly by using the command `jac run main.jac -walk second_walker`. Here, the `-walk` parameter instructs the `jsctl` to execute a certain walker.

## Walkers Navigating Graphs Examples

As mentioned earlier the walkers can traverse(walk) through the nodes of the graph in breadfast search or depth first search approuches.

> **Note**
>
> BFS is a traversal approach in which begins from root node and walk through all nodes on the same level before moving on to the next level. DFS is also a traversal approach in which the traverse begins at the root node and proceeds through the nodes as far as possible until we reach the node with no unvisited nearby nodes.

Look at the following example;

![alt text](support\guide\lang_docs\images\traverse_graph_example.PNG "Example Graph - Navigating")

```
node plain: has name;

## defining the graph
graph example {
    has anchor head;
    spawn {
        n=[];
        for i=0 to i<7 by i+=1 {
            n.l::append(spawn node::plain(name=i+1));
        }

        n[0] --> n[1] --> n[2];
        n[1] --> n[3];
        n[0] --> n[4] --> n[5];
        n[4] --> n[6];
        head=n[0];
        }
    }

#init walker traversing
walker init {
    root {
        start = spawn here --> graph::example;
        take-->;
        }
    plain {
        std.out(here.name);
        take-->;
    }
}

```
`take` command lets the walker travers through graph nodes. By default, a walker travers with `take` command using the breadth-first search approach. But the `take` command is flexible hence you can indicate whether the take command should use a depth-first or a breadth-first traversal to navigate.

Look at the following example;

```
node plain: has name;

graph example {
    has anchor head;
    spawn {
        n=[];
        for i=0 to i<7 by i+=1 {
        n.l::append(spawn node::plain(name=i+1));
        }

        n[0] --> n[1] --> n[2];
        n[1] --> n[3];
        n[0] --> n[4] --> n[5];
        n[4] --> n[6];

        head=n[0];
        }
    }

walker walk_with_breadth {
    has anchor node_order = [];
    node_order.l::append(here.name);
    take:bfs -->; #take:b can also be used
    }

walker walk_with_depth {
    has anchor node_order = [];
    node_order.l::append(here.name);
    take:dfs -->; #take:d can also be used
    }

walker init {
    start = spawn here --> graph::example;
    b_order = spawn start walker::walk_with_breadth;
    d_order = spawn start walker::walk_with_depth;
    std.out("Walk with Breadth:",b_order,"\nWalk with Depth:",d_order);
    }
```

Output:

```
jaseci > jac run main.jac
Walk with Breadth: [1, 2, 5, 3, 4, 6, 7] 
Walk with Depth: [1, 2, 3, 4, 5, 6, 7]
```

## Skipping

The idea behind the abstraction of `skip` in the context of a walkers code block is that it tells a walker to halt and abandon any unfinished work on the current node in favor of moving to the next node (or complete computation if no nodes are queued up).

Node/edge abilities also support the usage of the skip directive. The skip merely decides not to use the remaining steps of that `ability` itself in this context.

Lets look at an example of a walker using the skip command.

```
global node_count=0;
node simple: has id;

walker init {
    has output = [];
    with entry {
        t = here;
        for i=0 to i<10 by i+=1 {
            t = spawn t --> node::simple(id=global.node_count);
        global.node_count+=1;
        }
        }
    take -->;
    simple {
        if(here.id % 2==0): skip;
            output.l::append(here.id);
    }
    output.l::append(here.info['name']);
    with exit: std.out(output);
    }
```
In the above code; skips the code execution when the node id is an even number.

## Disengaging 

The command `disengage` tells the walker to stop all execution and "disengage" from the graph (i.e., stop visiting nodes anymore from here) and can only be used inside the code body of a walker.

Look at the example below;

```
global node_count=0;
node simple: has id;

walker init {
    has output = [];
        with entry {
        t = here;
        for i=0 to i<10 by i+=1 {
            t = spawn t --> node::simple(id=global.node_count);
        global.node_count+=1;
        }
        }
    take -->;
    simple {
    if(here.id % 2==0): skip;
        if(here.id == 7): disengage;
            output.l::append(here.id);
        }
        output.l::append(here.info['name']);
    with exit: std.out(output);
}

```




