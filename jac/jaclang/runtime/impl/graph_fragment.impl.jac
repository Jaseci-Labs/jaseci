impl GraphBuilder._add_node(value: Node) -> None {
    if not self.capture {
        return;
    }
    key = id(value);
    if key not in self._node_ids {
        self._node_ids.add(key);
        self._nodes.append(value);
    }
}

impl GraphBuilder.record_edges(values: list[Edge]) {
    for value in values {
        self.record_edge(value);
    }
}

impl GraphBuilder.record_edge(value: Edge) -> None {
    if not self.capture {
        return;
    }
    key = id(value);
    if key not in self._edge_ids {
        self._edge_ids.add(key);
        self._edges.append(value);
    }
}
