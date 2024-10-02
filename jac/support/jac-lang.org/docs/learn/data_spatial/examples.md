# <span style="color: orange">Examples
## <span style="color: orange">Node Creation and Connections
Nodes can be connected in various ways, including from a single node to a list of nodes, a list of nodes to a single node, a list of nodes to another list of nodes, or even a single node to a single node
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/data_spatial/create_node.jac"
    ```
??? example "Graph Image"
    ![Image](Images/create_node.png)

##  <span style="color: orange">Custom Edge Creation and Operations
We can establish connections between nodes or lists of nodes using custom edges instead of the default generic edges, allowing for more control and customization in the relationships between nodes.

=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/data_spatial/custom_edge.jac"
    ```
Lines 17-21 demonstrate how to retrieve visitable or reachable nodes from a given node by applying specific edge conditions, such as filtering based on edge types or chaining multiple edge traversals.
??? example "Graph Image"
    ![Image](Images/custom_edge.png)

## <span style="color: orange">Filtering
We can filter specific types of nodes from a list of visitable nodes based on their type, and further apply conditions on node attributes to refine the results.
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/data_spatial/filtering.jac"
    ```
??? example "Graph Image"
    ![Image](Images/filtering.png)

##  <span style="color: orange">Visiting
We can retrieve all visitable nodes from a node in specific directions.
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/data_spatial/visiting.jac"
    ```
??? example "Graph Image"
    ![Image](Images/visiting.png)

##  <span style="color: orange">Walker Definition
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/data_spatial/define_walker.jac"
    ```
??? example "Graph Image"
    ![Image](Images/define_walker.png)

