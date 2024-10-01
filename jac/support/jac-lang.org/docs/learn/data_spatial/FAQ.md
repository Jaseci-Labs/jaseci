??? question "What is node and how to define a node?"
    - Nodes are archetypes that form part of a graph. They can hold properties. You define nodes with attributes and values:
    ```jac
      node node_name{
          has node_property: int;
      }
      node node_name{
          has node_property: int = 10;
      }
    ```

??? question "How to delete a node? "
    - You can delete a node using:
    ```jac
        del node_name;
    ```

??? question "How to connect two nodes?"
    - Nodes can be connected using generic edges (default) or custom edges (defined with specific properties). 
    ```jac
      node_1 ++> node_2; # uni directional edge
      node_1 <++> node_2; # bidirectional edge
    ```

??? question "What is custom edge?"
    - When we connect nodes simply, they are connected using generic edge. In Jac, we can connect nodes with our custom edges in which custom edge can have prefered properties and abilities, allowing more control over the relationships between nodes.
    ```jac
      edge edge_name{
          has edge_property: int = 10;
      }
    ```

??? question "How to connect nodes with custom edge?"
    - To connect nodes using custom edges:
    ```jac
      # connect without specifying property value
      node_1 +: edge_name :+> node_2;
      # connect with specific property value
      node_1 +: edge_name :edge_property= 15: +> node_2;
    ```

??? question "How to delete connection/edge between two nodes?"
    - Connections between nodes can be removed:
    ```jac
      node_1 del --> node_2;
    ```

??? question "What is walker and how to define a walker?"
    - A walker is an archetype that performs actions within the graph. It can traverse nodes through edges, performing operations at each step.
    ```jac
    walker walker_name {
      can walker_ability with `specific_node entry;
    }
    ```

??? question "How to visit all the Successor nodes of a node/ list of nodes?"
    - A walker can visit all successor nodes (directly connected nodes):
      ```jac
          visit [node_name -->];
      ```

??? question "How to get all the Successor nodes of a node/ list of nodes?"
    - You can also retrieve all the successor nodes:
      ```jac
          print([node_name -->]);
      ```

??? question "How to get all edges that is connected with a node?"
    - To get all edges connected to a node:
    ```jac
        print(:e:[node_1[0]-->],:e:[node_1[0]<--]);
    ```

??? question "How to get all edges that is connected between two nodes?"
    - To get all edges between two nodes:
    ```jac
        print(:e:[node_1[0]-->node_2]);
    ```

??? question "How to connect list of nodes with a single node in series or parallel"
    - Nodes can be connected in series or parallel:
    ```jac
        # Series
        node_1 ++> node_list[0];
        for i to i < length(node_list) by i+=1 {
            node_list[i] ++> node_list[i+1];
        }
        # Parallel
        node_1 ++> node_list;
    ```

??? question "How to make mesh with two list of nodes"
    ```jac
        node_list_1 ++> node_list_2;
    ```

??? question "How to spawn a walker from root?"
    - You can spawn a walker from a specific node or root:
    ```jac
        with entry {
          root spawn walker_name();
        }
    ```

??? question "How to setup special ability for a entry through a given node or root?"
    - You can set up special abilities for root or specific node entries in walkers:
    ```jac
        # Entry through root
        walker  walker_name {
          can walker_ability with `root entry;
        }
        # Entry through a given node
        walker  walker_name {
          can walker_ability with specific_node entry;
        }
        # Entry through root or a given node
        walker  walker_name {
          can walker_ability with `root | specific_node entry;
        }
    ```

??? question "How to setup special ability of a node for a certain walker?"
    - You can setup special ability of a node for a certain walker using:
    ```jac
        node  node_name {
          can node_ability with walker_name entry;
        }
    ```

??? question "How to get current architype?"
    - Current architype can be got using `self` keyword within that architype.
    ```jac
        print(self);
    ```

??? question "How to get current walker?"
    - Current walker can be get using `here` keyword within any node.
    ```jac
        print(here);
    ```

??? question "How to inherit walker?"
    - Walkers can inherit from other walkers and override their abilities:
    ```jac
        walker walker_1{
        }
        walker walker_2 : walker_1:{
        }
    ```

??? question "How to override walker ability?"
    - To override a walker’s ability:
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


