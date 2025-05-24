### Visit Statements
Visit statements in Jac implement the fundamental data spatial operation that enables walkers to traverse through node-edge topological structures. This statement embodies the core Data Spatial Programming (DSP) paradigm of "computation moving to data" rather than the traditional approach of moving data to computation.

**Theoretical Foundation**

In DSP theory, the visit statement ($\triangleright$) allows walkers to move between nodes and edges in the topological structure, representing the dynamic traversal capability central to the paradigm. Walkers are autonomous computational entities that traverse node-edge structures, carrying state and behaviors that execute based on their current location.

**Basic Visit Syntax**

The basic syntax for visit statements follows this pattern:
```jac
visit target [else fallback_block]
```

**Directional Visit Patterns**

The example demonstrates directional traversal using arrow notation:
```jac
visit [-->] else {
    visit root;
    disengage;
}
```

The `[-->]` syntax represents traversal along outgoing edges from the current node. This pattern enables walkers to:

- **Explore connected nodes**: Move to nodes reachable via outgoing edges
- **Follow topological paths**: Traverse the graph structure according to connection patterns
- **Implement search algorithms**: Use systematic traversal to locate specific nodes or data

**Conditional Traversal with Else Clauses**

Visit statements support else clauses that execute when the primary visit target is unavailable:

- **Fallback behavior**: When `[-->]` finds no outgoing edges, the else block executes
- **Graceful handling**: Provides alternative actions when traversal paths are exhausted
- **Control flow**: Enables complex navigation logic with built-in error handling

**Walker Abilities and Visit Integration**

The example shows a walker ability that automatically triggers visit behavior:
```jac
walker Visitor {
    can travel with `root entry {
        visit [-->] else {
            visit root;
            disengage;
        }
    }
}
```

Key aspects:
- **Implicit activation**: The `travel` ability triggers automatically when the walker enters a root node
- **Context-sensitive execution**: Behavior adapts based on the walker's current location
- **Distributed computation**: Logic executes at data locations rather than centralized functions

**Node Response to Walker Visits**

Nodes can define abilities that respond to walker visits:
```jac
node item {
    can speak with Visitor entry {
        print("Hey There!!!");
    }
}
```

This demonstrates:
- **Location-bound computation**: Nodes contain computational abilities triggered by visitor arrival
- **Type-specific responses**: Different behaviors for different walker types
- **Bidirectional interaction**: Both walkers and nodes participate in computation

**Traversal Lifecycle**

The complete traversal process involves:

1. **Walker spawning**: `root spawn Visitor()` activates the walker at the root node
2. **Ability triggering**: The walker's `travel` ability executes upon entry
3. **Visit execution**: The walker moves to connected nodes via `visit [-->]`
4. **Node response**: Each visited node's `speak` ability triggers
5. **Fallback handling**: If no outgoing edges exist, the else clause executes
6. **Termination**: `disengage` removes the walker from active traversal

**Data Spatial Benefits**

Visit statements enable several key advantages:

- **Natural graph algorithms**: Traversal logic maps directly to problem domain topology
- **Decoupled computation**: Algorithms separate from data structure implementation
- **Context-aware processing**: Computation adapts to local data and connection patterns
- **Intuitive control flow**: Navigation follows the natural structure of connected data

**Common Patterns**

Visit statements support various traversal patterns:
- **Breadth-first exploration**: Systematic traversal of all reachable nodes
- **Depth-first search**: Following paths to their conclusion before backtracking  
- **Conditional navigation**: Choosing paths based on node properties or walker state
- **Cyclic traversal**: Returning to previously visited nodes for iterative processing

The provided example demonstrates a simple breadth-first traversal where a walker visits all nodes connected to the root, printing a message at each location. This illustrates how visit statements transform graph traversal from complex algorithmic implementation to intuitive navigation through connected data structures.

Visit statements represent a fundamental shift in programming paradigms, enabling developers to express algorithms in terms of movement through data topologies rather than data manipulation through function calls.
