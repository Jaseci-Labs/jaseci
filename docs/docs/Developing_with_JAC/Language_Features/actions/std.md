---
title :  Standard  Actions
---

```jac 

# printing output to log
data = {
    "type" : "String",
    "name" " "Jaseci"
}
result  = std.log(data)

```
```jac 
data = {
    "type" : "String",
    "name" " "Jaseci"
}

# print on to the termnial
std.out(data)

```

```jac 
# takes input from the terminal 
# any string passed will be printed on to the screen
std.input("> ")
```
```jac 
# printing to standard error

std.eer()

```

```jac 
# Sorts in place list of lists by column
# Param 1 - list
# Param 2 - col number
# Param 3 - boolean as to whether things should be reversed
#Return - Sorted list
sorted_list = std.sort_by_col()

```

```jac 
# Get utc date time for now in iso format
time  = std.time_now()

```

```jac 

# set global varibale visible to all walker
# name : string
# value : value (must be json seriaziable)

global_variable = std.set_global(name,value);

```

```jac 
# get global variable
# name : name of variable
global_variable = std.get_global(name);

```
### Load local actions to Jaseci
```jac 
# load local actions date to jaseci
action = std.actload_local("date.py");

```

### Load remote actions to Jaseci
```jac
action = std.actload_remote(url)

```
### Load module actions to Jaseci
```jac
#load use_qa model
action = std.actload_module('use_qa');
```
### Destroy Global
```jac 
global = std.destroy_global(name)
```

### Set object Permission
```jac 
element - target element
mode - valid permission (public, private, read_only)
object = std.set_perms(element,mode)
```

### Get object Permission

```jac
#Returns object access mode for any Jaseci object
# object - target element
# Return - Sorted list

obj = std.get_perms(object);
```

###  Grant object Permission

```jac
# grants another user permission to access a jaseci object
# obj :target element
# element : master to be granted permission
# readonly : Boolean read-only flag
# Returns sorted list

object  = std.grant_perms(obj,element,readonly)
```
### Revoke Permission
```jac 
# Remove permission for user to access a jaseci object
# obj : target element
# element : master to be revoke permission
# return sorted list
objects = std.revoke_perms(obj,element);
```

### Get Report
```jac 
# Get current report so far from walker run

reprt = std.get_report();

```
