# Edge abilities in Jaseci

Edges in Jaseci can have abilities, which are self-contained in-memory/in-data compute operations. The body of an ability is specified within the specification of the edge using opening and closing braces ( { } ).

Abilities in Jaseci are similar to methods in traditional object-oriented programming, but with some differences in their semantics. An ability can only interact with the context and local variables of the edge it is affixed to and does not have a return semantic. However, it's worth noting that abilities can always access the scope of the executing walker using the special visitor variable.

Here's an example of an edge with an ability: