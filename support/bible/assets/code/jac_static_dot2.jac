node year {
    has color;
}
node month {
    has count, season;
}
node week;
node day;
edge parent;
edge child;
graph test_graph {
    has anchor A;
    strict graph G {
        H [node=year]
        C [node=week]
        E [node=day]
        D [node=day]

        A -> B // Basic directional edge
        B -- H // Basic non-directional edge
        B -> C [edge=parent] // Edge with attribute
        C -> D -> E [edge=child] // Chain edge

        A [color=red] // Node with DOT builtin graphing attr
        B [node=month, count=2] [season=spring]// Node with Jac attr
        A [node=year] // Multiple attr statement per node
    }
}
walker init {
    root {
        spawn here --> graph::test_graph;
    }
    take -->;
    report here.details['name'];
}