- What is node and how to define a node?
  - It is an archetype that can be part of a graph object structure.
  ```jac
    node node_name{
        has node_property: int;
    }
    node node_name{
        has node_property: int = 10;
    }
  ```

- How to delete a node?
    ```jac
        del node_name;
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
  
- How to delete connection/edge between two nodes?
  ```jac
    node_1 del --> node_2;
  ```

- What is walker and how to define a walker?
  - It is used to define archetypes that perform actions or traverse nodes and edges within a graph.
  ```jac
  walker walker_name {
    can walker_ability with `specific_node entry;
  }
    ```
- How to visit all the Successor nodes of a node/ list of nodes?
    ```jac
        visit [node_name -->];
    ```

- How to get all the Successor nodes of a node/ list of nodes?
    ```jac
        print([node_name -->]);
    ```

- How to get all edges that is connected with a node?
  ```jac
      print(:e:[node_1[0]-->]);
  ```

- How to get all edges that is connected between two nodes?
  ```jac
      print(:e:[node_1[0]-->node_2]);
  ```

- How to connect list of nodes with a single node in series
  ```jac
      node_1 ++> node_list[0];
      for i to i < length(node_list) by i+=1 {
          node_list[i] ++> node_list[i+1];
      }
  ```
  
- How to connect list of nodes with a single node in parallel
  ```jac
      node_1 ++> node_list;
  ```

- How to make mesh with two list of nodes
  ```jac
      node_list_1 ++> node_list_2;
  ``` 

- How to spawn a walker from root?
  ```jac
      with entry {
        root spawn walker_name();
      }
  ```

- How to setup special ability for root entry?
  ```jac
      walker  walker_name {
        can walker_ability with `root entry;
      }

  ```

- How to setup special ability for a entry through a given node?
  ```jac
      walker  walker_name {
        can walker_ability with specific_node entry;
      }

  ```

- How to setup special ability for a entry through a given node or root?
  ```jac
      walker  walker_name {
        can walker_ability with `root | specific_node entry;
      }

  ```

- How to setup special ability of a node for a certain walker?
  ```jac
      node  node_name {
        can node_ability with walker_name entry;
      }

  ```

- How to get current node?
  ```jac
      print(self);
  ```

- How to get current walker?
  ```jac
      print(self);
  ```

- How to inherit walker?
  ```jac
      walker walker_1{

      }

      walker walker_2 : walker_1:{

      }

  ```

- How to override walker ability?
  ```jac
      walker walker_1{
        can ability_1 with `root entry{
            print("write");
        }
      }

      walker walker_2 : walker_1:{
        override can ability_1 with `root entry{
            print("override");
        }
      }

  ```

- How to visit to a specific node
  ```jac
      visit[-->](`?node_1);
  ```



