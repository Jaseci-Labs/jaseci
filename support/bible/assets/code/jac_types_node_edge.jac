walker init {
    nd = spawn here ++> node::generic;
    std.out(nd.type, nd);
    std.out(nd.edge.type, nd.edge);
    std.out(nd.edge[0].type, nd.edge[0]);
}