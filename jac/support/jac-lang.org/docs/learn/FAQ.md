- How to define a node?
  ```jac
    node node_name{
        has node_property: int;
    }
    node node_name{
        has node_property: int = 10;
    }
  ```
  
- How to connect two nodes?
  ```jac
    # uni direction
    node_1 ++> node_2;
    # bidirection
    node_1 <++> node_2;
  ```

- What is custom edge?
  - When we connect nodes simply, they are connected using generic edge. In Jac, we can connect nodes with our custom edges in which we can have our prefered properties and abilities for edge.
  ```jac
    edge edge_name{
        has edge_property: int = 10;
    }
  ```
  
- How to connect nodes with custom edge?
  ```jac
    # connect without specifying property value
    node_1 +: edge_name :+> node_2;
    # connect with specific property value
    node_1 +: edge_name :edge_property= 15: +> node_2; 
  ```
  
- How to delete a node?

- How to delete connection between two nodes?
  ```jac
    node_1 del --> node_2;
  ```
- How to connect list of nodes with single or list of nodes?
```jac
    for nodes in list_nodes{
       node_1 ++> nodes; 
    }
```

- How to get all the visitable nodes from a node/ list of nodes?
```jac
    walker {
        visit [-->];
        print(here);
}
```
- How to get all edges that is connected between nodes?
```jac
    walker {
        print(here.edges());
    }
```


