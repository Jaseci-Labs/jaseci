# Graphs

In Jaseci, we elect to assume the following semantics for the graphs in Jaseci:

1. Graphs are directed with a special case of a doubly directed edge
type which can be utilized practically as an undirected edge.
2. Both nodes and edges have their own distinct identities (i,e. an edge isn’t representable
as a pairing of two nodes). This point is important as both nodes and edges can have
contexts.
3. Multigraphs (i.e., parallel edges) are allowed, including self-loop edges.
4. Graphs are not required to be acyclic.
5. No hypergraphs, as I wouldn’t want Jaseci programmers heads to explode.