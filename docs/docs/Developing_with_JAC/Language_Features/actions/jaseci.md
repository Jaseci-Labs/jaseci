---
title :  Jaseci Actions
---
## Alias
Alias provides names  for long string like UUIDs.

### Register Alias 
```jac 
#name (str): The name for the alias created by caller.
#value (str): The value for that name to map to (i.e., UUID)
response  = jaseci.alias_register(name,value);

```
### List Aliases
```jac 
# List all string to string alias that caller can use
jaseci.alias_list()

```

### Delete Alias 

```jac
# Delete an active string to string alias mapping
# name (str): The name for the alias to be removed from caller.
jaseci.alias_delete()
```
### Clear Alias
```jac 
#  Removes  all aliases.
jaseci.alias_clear()

```
## Objects

### Get global Variable
```jac 
# name: name of global variable
value = jaseci.global_get(name);

```

### Object Details 
```jac
# retuen detail of jaseci object
object : element - jaseci object
details = jaseci.object_get(object);
```

### Object Access Mode 

```jac 
# Get the object access mode for any jaseci object.
# object : element - jaseci object
accessMode  = jaseci.object_perms_set(object)

```

### Set Object access mode 

```jac 
# valid perms = ["public", "private", "read_only"]
# object : element - jaseci object
# perm : string 
jaseci.object_perms_set(element,perm);
```

### Object access grant

```jac
# grants one object the acess to another object
# object : element - object to access
# master : element  - object to gain access

rent = jaseci.object_perms_grant(element, master);

```
### Revoke object access

```jac
#Remove permissions for user to access a Jaseci object
# object : element - object that was  accessed
# master : element  - object that has access.
ret = jaseci.object_perms_revoke(element,master);

```
## Graphs

### Create Graph
```jac
# Create a graph instance and return root node graph object
jaseci.graph_create()

```
### Get Graph Content
```jac 
# Return the content of the graph with mode
# Valid modes: {default, dot, }
# gph :graph - graph whose conten you need
# mode : string - "deafult" or "dot" , "default" by default
Contents = jaseci.graph_get(gph);

```
### List Graph Objects

```jac
#  Provide complete list of all graph objects (list of root node objects)
# detailed : boolean - if eac graph details are wanted
graph_info = jaseci.graph_list(detailed);

```
### Set Default Graph
```jac 
# set the default graph master should use
# gph : graph - graph to be default.
message = jaseci.graph_active_set(gph);

```
### Remove Default Graph
```jac 
# Unsets the default sentinel master should use
jaseci.graph_active_unset();
```

### Get Default Graph 
```jac
# detailed : boolean - default false , true to return graph details (optional)
grph = jaseci.graph_active_get()
```
### Delete Graph 
```jac 
# permantely  delete graph 
# grph : graph - graph to be deleted

message = jaseci.graph_delete(grph);
```
### Return Node Value
```jac 
# returns value of a given node
# nd : node : node whose value will be returned.
node_value =  jaseci.graph_node_get(nd);
```
### Set Node Value
```jac 
# Assigns values to member variables of a given node using ctx object
# nd : node : node to who a value will be assigned.
# ctx : dictionary - values to assign 

node_details = jaseci.graph_node_set(nd,ctx);
```
## Sentinels

### Register Sentinel 
```jac 
#Create blank or code loaded sentinel and return object
# name: str -  "default" when not specified,
#encoded: bool 
#auto_run: Auto_run is the walker to execute on register (assumes active graph is selected), default is "init"
#ctx: dict = {},
#set_active: bool = True,

sentel = jaseci.sentinel_regsiter(name,encoded,auto_run,ctx,set_active);

``` 

### Global Sentinel 
```jac 
#   Copies global sentinel to local master
#set_active : boolean - set sentinel to be active
# on_demand : boolean - 

sentl = jaseci.sentinel_pull(set_active);
```


### Get Sentinel 
```jac 
# Get a sentinel rendered with specific mode
#Valid modes: {default, code, ir, }
#snt : sentinel : sentinel to be rendered in specific mode.
#mode : str - mode sentinel will be in 
snt  = jaseci.sentinel_get(snt,mode);
```
### Set Sentinel Code
```jac 
# Set code/ir for a sentinel, only replaces walkers/archs in sentinel
# Needs more clarity
jaseci.sentinel_set();
```
### Sentinel List
```jac 
# Provides Completed list of all sentinel objects 

#snt_list = jaseci.sentinel_list();
```
### Sentinel Test
```jac 
# Run battery of test cases within sentinel and provide result
#snt : sentinel - sentinel to be tested

snt_details = jaseci.sentinel_test(snt);
```
### Default Sentinel
```jac
# Sets the default sentinel master should use
#snt :sentinel - sentinel to be made default

message = jaseci.sentinel_active_set(snt);
```

### Remove Default Sentinel
```jac 
# Unsets the default sentinel master should use
messsage = jaseci.sentinel_active_unset();
```

### Set Global Sentinel 
```jac 
# Sets the default master sentinel to the global sentinel
response  = jaseci.sentinel_active_global();
```
### Return default Sentinel
```jac 
#  Returns the default sentinel master is using
response = jaseci.sentinel_active_get();
```

### Delete Sentinel
```jac 
# Permanently delete sentinel with given id
snt : sentinel - sentinel to be deleted

message = jaseci.sentinel_delete(snt);
```


