# Net Actions

This collection of actions provides standard operations that can be performed on graph elements such as nodes and edges. Several of these actions accept lists that exclusively consist of defined archetype nodes and/or edges. It's essential to note that a **jac_set** is simply a list that only contains such elements.

### Max Anchor Value
```jac
# returns object (node,edge) with the highest  anchor value
node year {
    has_anchor year_num;
}

jacset  = [year1,year2,year3];
value = net.max(jac_set);
```
### Minimum Anchor Value
```jac
# returns object (node,edges) with the lowest anchor value
node year {

    has_anchor year_num;
}

jacset  = [year1,year2,year3];
value = net.min(jac_set);
```
### Get Node Root
```jac
# returns root node of a given graph
node year {
    has_anchor year_num;
}

jacset  = [year1,year2,year3];
value = net.root(jac_set);
```
### Net Pack
The Net Pack function takes a JacSet object containing a collection of nodes and creates a generic dictionary representation of the subgraph, including all edges between nodes inside the collection. The packed dictionary format retains the complete context of all nodes and connecting edges. Any edges connecting nodes outside of the list of nodes are omitted from the packed subgraph representation. The resulting packed graph is portable and can be used for various use cases such as exporting graphs and subgraphs to be imported using the Net Unpack function.

#### Parameters
**item_set**: A JacSet object that contains a list of nodes comprising the subgraph to be packed. Edges can be included in this list but are ultimately ignored. All edges from the actual nodes in the context of the source graph will be automatically included in the packed dictionary if it connects two nodes within this input list.
**destroy**: A boolean flag indicating whether the original graph nodes covered by the pack operation should be destroyed.
#### Returns
A generic and portable dictionary representation of the subgraph.
```jac
args: item_set: JacSet (*req), destroy: bool (False)
```
### Net Unpack
The Net Unpack function takes a dictionary in the format produced by the Net Pack function and instantiates a set of nodes and edges corresponding to the subgraph represented by the packed action. The original contexts that were packed will also be created. It is important to note that when using this Net Unpack function, the unpacked collections of elements returned must be connected to a source graph to avoid memory leaks.

#### Parameters
**graph_dict**: A dictionary in the format produced by the Net Pack function.
#### Returns
A list of the nodes and edges that were created corresponding to the input packed format. Note that this list must be connected to a source graph to avoid memory leaks.
```jac
args: graph_dict: dict (*req)
```


