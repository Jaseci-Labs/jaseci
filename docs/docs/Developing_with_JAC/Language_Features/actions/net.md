# Net Actions 
### Max Anchor Value
```jac
# returns object (node,edge) with the highest  anchor value
node year {
    has_anchor year_num;
}

jacset  = [year1,year2,year3];
value = net.max(jac_set)
```
### Minimum Anchor Value
```jac
# returns object (node,edges) with the lowest anchor value
node year {
  
    has_anchor year_num;
}

jacset  = [year1,year2,year3];
value = net.min(jac_set)
```
### Get Node Root
```jac
# returns root node of a given graph 
node year {
    has_anchor year_num;
}

jacset  = [year1,year2,year3];
value = net.root(jac_set)
```