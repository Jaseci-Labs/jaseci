### Data Spatial References

Data spatial references provide specialized syntax for navigating and manipulating topological structures, enabling direct expression of graph relationships and traversal patterns. These references make topological relationships first-class citizens in the programming model.

#### Edge Reference Syntax

Edge references use square bracket notation with directional operators to express graph navigation:

```jac
[-->]                    # All outgoing edges
[<--]                    # All incoming edges  
[<-->]                   # All bidirectional edges
[-->:EdgeType:]          # Typed outgoing edges
[node --> target]        # Specific edge path
```

The square bracket syntax creates collections of edges or nodes that can be used for traversal, filtering, or manipulation operations.

#### Directional Navigation

Directional operators express the flow of relationships within the graph:

**Outgoing (`-->`)**: References edges that originate from the current node, representing relationships where the current node is the source.

**Incoming (`<--`)**: References edges that terminate at the current node, representing relationships where the current node is the target.

**Bidirectional (`<-->`)**: References edges that can be traversed in either direction, representing symmetric relationships.

#### Edge Connection Operations

Connection operators create new edges between nodes, establishing topological relationships:

```jac
source_node ++> target_node;                    # Create directed edge
source_node <++ target_node;                    # Create reverse directed edge
source_node <++> target_node;                   # Create bidirectional edge
source_node ++>:EdgeType(weight=5):++> target;  # Create typed edge with data
```

These operators enable dynamic graph construction where relationships can be established programmatically based on computational logic.

#### Edge Disconnection Operations

The `del` operator removes edges from the graph structure:

```jac
del source_node --> target_node;    # Remove specific edge
del [-->];                          # Remove all outgoing edges
del [<--:FollowEdge:];             # Remove typed incoming edges
```

Disconnection operations maintain graph integrity by properly cleaning up references and ensuring consistent topological state.

#### Filtered References

Edge references support inline filtering for selective graph operations:

```jac
[-->(weight > threshold)]           # Edges meeting weight criteria
[<--(target.active == true)]       # Incoming edges from active nodes
[<-->(`ConnectionType)]             # Edges of specific type
[-->(?name.startswith("test"))]     # Edges to nodes with test names
```

Filtering enables precise graph queries that combine topological navigation with data-driven selection criteria.

#### Integration with Walker Traversal

Data spatial references integrate seamlessly with walker traversal patterns:

```jac
walker NetworkAnalyzer {
    has visited: set = set();
    
    can explore with entry {
        # Mark current node as visited
        self.visited.add(here);
        
        # Find unvisited neighbors
        unvisited_neighbors = [-->] |> filter(|n| n not in self.visited);
        
        # Continue traversal to unvisited nodes
        if (unvisited_neighbors) {
            visit unvisited_neighbors;
        }
        
        # Analyze connection patterns
        strong_connections = [<-->:StrongEdge:];
        weak_connections = [<-->:WeakEdge:];
        
        # Report analysis results
        report {
            "node_id": here.id,
            "strong_count": len(strong_connections),
            "weak_count": len(weak_connections)
        };
    }
}
```

#### Type-Safe Graph Operations

References support type checking and validation for robust graph manipulation:

```jac
node DataNode {
    has data: dict;
    has node_type: str;
}

edge ProcessingEdge(DataNode, DataNode) {
    has processing_weight: float;
    has edge_type: str = "processing";
}

walker TypedProcessor {
    can process with DataNode entry {
        # Type-safe edge references
        processing_edges = [-->:ProcessingEdge:];
        
        # Filtered by edge properties
        high_priority = processing_edges |> filter(|e| e.processing_weight > 0.8);
        
        # Continue to high-priority targets
        visit high_priority |> map(|e| e.target);
    }
}
```

#### Dynamic Graph Construction

References enable dynamic graph construction based on runtime conditions:

```jac
walker GraphBuilder {
    can build_connections with entry {
        # Analyze current node data
        similarity_threshold = 0.7;
        
        # Find similar nodes in the graph
        all_nodes = [-->*];  # Get all reachable nodes
        similar_nodes = all_nodes |> filter(|n| 
            calculate_similarity(here.data, n.data) > similarity_threshold
        );
        
        # Create similarity edges
        for similar_node in similar_nodes {
            similarity_score = calculate_similarity(here.data, similar_node.data);
            here ++>:SimilarityEdge(score=similarity_score):++> similar_node;
        }
    }
}
```

Data spatial references provide the foundational syntax for expressing topological relationships and enabling computation to flow naturally through graph structures, making complex graph algorithms both intuitive and maintainable.
