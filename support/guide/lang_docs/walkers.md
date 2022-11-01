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

## Walkers Navigating Graphs Examples

When we run a jac code, by default it's exucuting the `init` walker. Basically the `walker init` works as the main method in other programming language. save following code as `main.jac` and run the code in `jsctl` shell with `jac dot main.jac`

```
node person;

edge married;
edge family;
edge friend;

walker init{
    node1 = spawn here -[friend]-> node::person;
    node2 = spawn node1 -[married]-> node::person;
    spawn node2 -[family]-> node::person;
}
```

Output:

```
jaseci > jac dot main.jac
strict digraph root {
    "n0" [ label="n0:root"  ]
    "n1" [ label="n1:person"  ]        
    "n2" [ label="n2:person"  ]        
    "n3" [ label="n3:person"  ]        
    "n0" -> "n1" [ label="e0:friend" ] 
    "n1" -> "n2" [ label="e1:married" ]
    "n2" -> "n3" [ label="e2:family" ] 
}
```
As you can see, this code has executed the init walker. Now let's take the definition of nodes out of the `init` walker. So here we are creating another walker to define the example nodes; 

```
node person;
edge married;
edge family;
edge friend;

walker build_example{
    node1 = spawn here -[friend]-> node::person;
    node2 = spawn node1 -[married]-> node::person;
    spawn node2 -[family]-> node::person;
}

walker init{
    root{
        spawn here walker::build_example;
    }
}
```

You can see we get output similar to the previous code, here we are defining the nodes in the `build_example` walker and calling the `build_example` walker inside the `init` walker. Also we can directly run the `build example` walker using `jac dot main.jac -walk build_example`. Here the `-walk` argument tells the jsctl which walker should execute.

Look at the following example;

```

```
