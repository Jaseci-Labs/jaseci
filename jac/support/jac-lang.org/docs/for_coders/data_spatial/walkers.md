# <span style="color: orange">Walkers</span>
- Walkers are "worker bots" that move (walk) along the graph while performing tasks on the nodes they visit.
- They play a crucial role in executing visit-dependent abilities as discussed in nodes and facilitating interactions between graph nodes and themselves.

## Graph Traversal
- Walkers navigate the graph using the ```visit``` keyword.
- They can be spawned at any point on the graph with the ```spawn``` keyword.

## Attributes & Abilities
- Similar to nodes, walkers can have their own attributes and abilities including both callable and visit-dependent abilities.

- **Visit-dependent Abilities:** 
    - Ensures the ability is executed only when the walker visits a node.
    - Can be defined within:
        - **Nodes:** Triggered upon a walker's arrival.
        - **Walkers:**  Specific to the walker’s operation during its visit.

## Reference Keywords:
- ```self``` : Refers to the walker object itself.
- ```here```: References the current node visited by the walker, enabling access to its attributes and callable abilities.
    This allows seamless interaction between walker and node attributes.

- Control Movement:
    - Use ```visit``` to:
        - Direct the walker to a specific node.
        - Walk along an edge connecting nodes.

- Remove Walkers:
    - Use ```disengage``` to remove a walker from the graph.

## Walkers in Action:
- Walkers prioritize their visit-dependent abilities first before executing the abilities of the visited node.
- This enables flexible task delegation:
    - Define visit-dependent tasks either within the walker or in the node.

By using these principles, walkers can efficiently traverse and interact with graphs, enabling dynamic workflows.
