# Abstractions of Jaseci

There are a number of abstractions and concepts in Jac that is distinct from most (all?) other languages. These would be a good place to begin understanding for a seasoned / semi-seasoned programmer. In a nutshell...

- [Abstractions of Jaseci](#abstractions-of-jaseci)
  - [Graphs](#graphs)
  - [Walkers](#walkers)
  - [Abilities](#abilities)
  - [Here and Visitor](#here-and-visitor)
  - [Actions](#actions)


## Graphs

It is strange to see how our programming languages have evolved over the years, and yet, one fundamental data structure has been left behind. Almost every data structure used by programmers to solve problems can be represented as a graph or a special case of a graph, except for hash tables. This means that structures such as stacks, lists, queues, trees, heaps, and even graphs can be modeled with graphs. But, despite this, no programming language uses graph semantics as its first order data abstraction.

The graph semantic is incredibly rich and intuitive for humans to understand and is particularly well suited for conceptualizing and solving computational problems, especially in the field of AI. However, some may argue that there are graph libraries available in their preferred language and that a language forcing the concept is not necessary. To this, I argue that core design languages are based on their inherent abstractions, and with graphs not being one of them, the language is not optimized to allow programmers to easily utilize the rich semantics that graphs offer.

Another argument against using graphs as a first-order abstraction is that it might slow down the language. However, modern programming languages have absurd abstractions, such as dynamic typing, which have a higher runtime complexity than what would be needed to support graph semantics. Jaseci aims to revolutionize how we perceive data and memory by making graphs, with their intuitive and rich semantics, the foundational primitive for memory representation.

In Jaseci, we elect to assume the following semantics for the graphs in Jaseci:

1. Graphs are directed with a special case of a doubly directed edge
type which can be utilized practically as an undirected edge.
2. Both nodes and edges have their own distinct identities (i,e. an edge isn’t representable
as a pairing of two nodes). This point is important as both nodes and edges can have
contexts.
3. Multigraphs (i.e., parallel edges) are allowed, including self-loop edges.
4. Graphs are not required to be acyclic.
5. No hypergraphs, as I wouldn’t want Jaseci programmers heads to explode.

Refer to [Wikipedias description of graphs](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)) to learn more about graphs.

## Walkers

One of the major innovations in Jaseci is the concept of walkers. This abstraction has never been seen in any programming language before and offers a new perspective on programmatic execution.

In a nutshell, a walker is a unit of execution that retains state (its local scope) as it travels
over a graphs. Walkers *walk* from node to node in the graph and executing its body.
The walker’s body is specified with an opening and closing braces ( `{` `}` ) and is executed to
completion on each node it lands on. In this sense a walker iterates while spooling through a
sequence of nodes that it ‘takes’ using the take keyword. We call each of these iterations
node-bound iterations.

Variables in a walker's body are divided into two categories: context variables, which retain their values as the walker moves through the graph, and local variables, which are reinitialized for each node-bound iteration.

Walkers offer a different approach to programmatic execution, distinct from the common function-based model used in other languages. Instead of a function's scope being temporarily pushed onto a growing stack as functions call other functions, scopes in Jaseci can be laid out spatially on a graph and walkers can traverse the graph, carrying their scope with them. This new model introduces data-spatial problem solving, where walkers can access any scope at any time in a modular manner, unlike in the function-based model where scopes become inaccessible after a function is called until it returns.

When solving problems with walkers, a developer can think of that walker as a little self-contained robot or agent that can retain context as it spacially moves about a graph, interacting with the context in nodes and edges of that graph.

## Abilities

Nodes, edges, and walkers can have **abilities**. The body of an ability is specified with an
opening and closing braces ( `{` `}` ) within the specification of a node, edge, or walker and
specify a unit of execution.

Abilities are most closely analogous to methods in a traditional object oriented program,
however they do not have the same semantics of a traditional function. An ability can only
interact within the scope of context and local variables of the node/edge/walker for which it
is affixed and do not have a return semantic. (Though it is important to note, that abilities
can always access the scope of the executing walker using the visitor special variable as
described below)

When using abilities, a developer can think of these as self-contained in-memory/in-data
compute operations.

## Here and Visitor

At every execution point in a Jac/Jaseci program there are two scopes visible, that of the
walker, and that of the node it is executing on. These contexts can be referenced with the
special variables `here` and `visitor` respectively. Walkers use `here` to refer to the context of
the node it is currently executing on, and abilities can use `visitor` to refer to the context of
the current walker executing. Think of these are special `this` references.

## Actions

Actions enables bindings to functionality specified outside of Jac/Jaseci and behave as function
calls with returns. These are analogous to library calls in traditional languages. This external
functionality in practice takes the form of direct binding to python implementations that are
packaged up as a Jaseci action library.


> **Note**
>
> This action interface is the abstraction that allows Jaseci to do it's sophisticated serverless inter-machine optimizations, auto-scaling, auto-componentization etc.
