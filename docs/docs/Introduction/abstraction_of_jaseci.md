# Graphs, The Uninvited Guest at Every Party

It is strange to see how our programming languages have evolved over the years, and yet, one fundamental data structure has been left behind. Almost every data structure used by programmers to solve problems can be represented as a graph or a special case of a graph, except for hash tables. This means that structures such as stacks, lists, queues, trees, heaps, and even graphs can be modeled with graphs. But, despite this, no programming language uses graph semantics as its first order data abstraction.

The graph semantic is incredibly rich and intuitive for humans to understand and is particularly well suited for conceptualizing and solving computational problems, especially in the field of AI. However, some may argue that there are graph libraries available in their preferred language and that a language forcing the concept is not necessary. To this, I argue that core design languages are based on their inherent abstractions, and with graphs not being one of them, the language is not optimized to allow programmers to easily utilize the rich semantics that graphs offer.

Another argument against using graphs as a first-order abstraction is that it might slow down the language. However, modern programming languages have absurd abstractions, such as dynamic typing, which have a higher runtime complexity than what would be needed to support graph semantics.

# Putting It All in Perspective: A New Way of Viewing Data and Memory

Jaseci aims to revolutionize how we perceive data and memory by making graphs, with their intuitive and rich semantics, the foundational primitive for memory representation.

## Introducing Walkers: A Unique Abstraction

One of the major innovations in Jaseci is the concept of walkers. This abstraction has never been seen in any programming language before and offers a new perspective on programmatic execution.

A walker is a unit of execution that retains its local scope as it moves through a graph, executing its body on each node it visits. The body of the walker is defined using braces ( {} ) and is executed to completion on every node it reaches. The walker moves from node to node using the "take" keyword, making each iteration a node-bound iteration.

Variables in a walker's body are divided into two categories: context variables, which retain their values as the walker moves through the graph, and local variables, which are reinitialized for each node-bound iteration.

Walkers offer a different approach to programmatic execution, distinct from the common function-based model used in other languages. Instead of a function's scope being temporarily pushed onto a growing stack as functions call other functions, scopes in Jaseci can be laid out spatially on a graph and walkers can traverse the graph, carrying their scope with them. This new model introduces data-spatial problem solving, where walkers can access any scope at any time in a modular manner, unlike in the function-based model where scopes become inaccessible after a function is called until it returns.

Think of walkers as tiny self-contained robots or agents that can retain context as they move through a graph, interacting with the context of nodes and edges.

In addition to the "take" command, which introduces new control flow options for node-bound iterations, Jaseci also introduces the keywords "disengage," "skip," and "ignore." These keywords allow walkers to stop walking the graph, skip over a node for execution, or ignore certain paths in the graph. These semantics are described in further detail in later chapters.