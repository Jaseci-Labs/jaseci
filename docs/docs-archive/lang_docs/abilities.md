# Abilities

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