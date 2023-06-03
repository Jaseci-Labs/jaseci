---
sidebar_position: 3
title: JEP 3 - Ability to Easily Traverse and Reference Nodes
---

### JEP 3 - Ability to Easily Traverse and Reference Nodes
---
#### Details
| Author      | Type | Quick Description | 
| ----------- | ------ | ------ |
| Chandra | Technical | Ability to Easily Traverse and Reference Nodes |

#### Description

Currently, it can be challenging to traverse to a node that is distant from the current node, especially when there is no direct edge connecting them. One would need to traverse the entire graph to locate the desired node. However, what if we establish connections between every node by default, forming a complete graph with predefined bidirectional edges? This way, you would simply need to specify the property of the node you seek to visit, and the walker would automatically navigate to the node where that property holds true.

For example, suppose you have a graph with nodes representing people and edges representing relationships between them. In that case, you could easily traverse to a node representing a person with a specific name by specifying the name property of the node you seek to visit. This would be possible because the walker would automatically traverse to the node where the name property holds true.

```jac
walker find_people {
    has name;
    person_node = node::person(name=="chandra"); 
    std.out(person_node.name); // chandra
    // this will return the reference to the node with name "chandra". doesnt matter where it is in the graph.'
    // whether it is connected to the current node or not. This can be done because we have a complete graph. with generic bidirectional edge between every node.
}
```