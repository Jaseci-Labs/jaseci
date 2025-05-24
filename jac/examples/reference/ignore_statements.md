Ignore statements provide a mechanism to exclude specific nodes or edges from walker traversal paths. This feature enables selective graph navigation by marking elements that should be skipped during traversal operations.

#### Syntax

```jac
ignore expression;
```

#### Purpose

Ignore statements allow walkers to:
- Skip specific nodes during traversal
- Exclude edges from path consideration
- Create filtered traversal patterns
- Optimize navigation by avoiding irrelevant paths

#### Basic Usage

```jac
walker Traverser {
    can traverse with entry {
        # Ignore specific nodes
        ignore here.blocked_nodes;
        
        # Visit all other connected nodes
        visit [-->];
    }
}
```

#### Ignoring Nodes

Mark nodes to be skipped:

```jac
walker Searcher {
    has visited: set = {};
    
    can search with entry {
        # Avoid revisiting nodes
        if here in self.visited {
            return;
        }
        self.visited.add(here);
        
        # Ignore nodes marked as inactive
        inactive = [-->(?.active == False)];
        ignore inactive;
        
        # Visit only active nodes
        visit [-->];
    }
}
```

#### Ignoring Edges

Exclude specific connections:

```jac
walker PathFinder {
    can find_path with entry {
        # Ignore low-weight edges
        weak_edges = [-->(?.weight < 0.5)];
        ignore weak_edges;
        
        # Traverse only strong connections
        visit [-->];
    }
}
```

#### Conditional Ignoring

Dynamic exclusion based on conditions:

```jac
walker ConditionalTraverser {
    has security_level: int;
    
    can traverse with entry {
        # Ignore nodes above security clearance
        restricted = [];
        for n in [-->] {
            if n.required_level > self.security_level {
                restricted.append(n);
            }
        }
        ignore restricted;
        
        # Visit accessible nodes
        visit [-->];
    }
}
```

#### Pattern-Based Ignoring

Use type and property filters:

```jac
walker TypedExplorer {
    can explore with entry {
        # Ignore specific node types
        ignore [-->(`BlockedType)];
        
        # Ignore nodes matching pattern
        ignore [-->(?.category == "excluded")];
        
        # Visit remaining nodes
        visit [-->];
    }
}
```

#### Integration with Visit

Combine ignore and visit for precise control:

```jac
walker SmartNavigator {
    can navigate with entry {
        all_neighbors = [-->];
        
        # Categorize nodes
        high_priority = [];
        low_priority = [];
        blocked = [];
        
        for n in all_neighbors {
            if n.priority > 0.8 {
                high_priority.append(n);
            } elif n.priority > 0.3 {
                low_priority.append(n);
            } else {
                blocked.append(n);
            }
        }
        
        # Ignore low-value nodes
        ignore blocked;
        
        # Visit high priority first
        visit high_priority;
        visit low_priority;
    }
}
```

#### Temporary Ignoring

Ignore within specific contexts:

```jac
walker ContextualWalker {
    has ignore_list: list = [];
    
    can process with entry {
        # Temporarily ignore nodes
        if here.is_checkpoint {
            self.ignore_list = here.get_blocked_paths();
        }
        
        # Apply current ignore list
        ignore self.ignore_list;
        
        # Clear ignore list at boundaries
        if here.is_boundary {
            self.ignore_list = [];
        }
        
        visit [-->];
    }
}
```

#### Performance Optimization

Use ignore to prune search spaces:

```jac
walker EfficientSearcher {
    has max_cost: float;
    has current_cost: float = 0.0;
    
    can search with entry {
        # Update path cost
        self.current_cost += here.cost;
        
        # Ignore paths exceeding budget
        expensive_paths = [];
        for n in [-->] {
            if self.current_cost + n.estimated_cost > self.max_cost {
                expensive_paths.append(n);
            }
        }
        ignore expensive_paths;
        
        # Continue with viable paths
        visit [-->];
        
        # Restore cost on exit
        self.current_cost -= here.cost;
    }
}
```

#### Relationship with Graph Structure

Ignore statements don't modify the graph:

```jac
walker Observer {
    can observe with entry {
        # Count all connections
        total_edges = len([-->]);
        
        # Ignore some nodes
        ignore [-->(?.temporary)];
        
        # Original graph unchanged
        assert len([-->]) == total_edges;
        
        # But traversal is filtered
        visit [-->];  # Skips ignored nodes
    }
}
```

#### Best Practices

1. **Clear Criteria**: Use explicit conditions for ignoring
2. **Document Reasons**: Explain why nodes are ignored
3. **Consider Alternatives**: Sometimes filtering in visit is clearer
4. **Reset State**: Clear ignore lists when appropriate
5. **Performance**: Ignore early to avoid unnecessary computation

#### Common Patterns

##### Visited Set Pattern
```jac
walker DepthFirst {
    has visited: set = {};
    
    can traverse with entry {
        self.visited.add(here);
        
        # Ignore already visited
        ignore [n for n in [-->] if n in self.visited];
        
        visit [-->];
    }
}
```

##### Type-Based Filtering
```jac
walker TypeFilter {
    has allowed_types: list;
    
    can filter with entry {
        # Ignore non-matching types
        for t in self.allowed_types {
            ignore [-->(!`t)];
        }
        
        visit [-->];
    }
}
```

##### Threshold-Based Pruning
```jac
walker ThresholdWalker {
    has min_score: float;
    
    can walk with entry {
        # Ignore low-scoring paths
        ignore [-->(?.score < self.min_score)];
        
        # Process high-scoring nodes
        visit [-->];
    }
}
```

Ignore statements provide essential control over traversal patterns, enabling efficient and targeted graph navigation while maintaining clean, readable code. They work in harmony with visit statements to create sophisticated traversal algorithms.
