# Standard Actions Library

### Logging output

Printing output to log.

```jac
data = {
    "type" : "String",
    "name" : "Jaseci"
};
result  = std.log(data);

```
### Output

Print on to the termnial.

```jac
data = {
    "type" : "String",
    "name" : "Jaseci"
};

std.out(data);
```
### Input

Takes input from the terminal.
Any string passed will be printed on to the screen.

```jac
std.input("> ");
```
### Js Input

Takes input from the terminal
Any string passed will be printed on to the screen

```jac
std.js_input("> ");
```
### Standar Error

Printing to standard error.

```jac
std.eer();
```
### Sort Columns

Sorts in place list of lists by column.
`Param 1` - list
`Param 2` - col number (optional)
`Param 3` - boolean as to whether things should be reversed (optional)
`Return` - Sorted list

```jac
sorted_list = std.sort_by_col(param1,param2);
```
### UTC time

Get utc date time for now in iso format.

```jac
time  = std.time_now();
```

### Set Global Variable

Set global varibale visible to all walker
`name` : `string`
`value` : value (must be json seriaziable)

```jac
global_variable = std.set_global(name,value);
```
### Get Global Variable

Get global variable.
`name` : name of variable.

```jac
global_variable = std.get_global(name);
```
### Load local actions to Jaseci

Load local actions date to jaseci.

```jac
action = std.actload_local("date.py");
```

### Load remote actions to Jaseci

```jac
action = std.actload_remote(url);
```
### Load module actions to Jaseci

Load `use_qa` model.

```jac
action = std.actload_module('use_qa');
```
### Destroy Global

```jac
global = std.destroy_global(name);
```

### Set object Permission

`element` - target element
`mode` - valid permission (public, private, read_only)

```jac
object = std.set_perms(element,mode);
```

### Get object Permission

Returns object access mode for any Jaseci object
`object` - target element

**Return**

Sorted list

```jac
obj = std.get_perms(object);
```

###  Grant object Permission

Grants another user permission to access a jaseci object.

`obj` :target element
`element` : master to be granted permission
`readonly` : Boolean read-only flag

Returns sorted list.

```jac
object  = std.grant_perms(obj,element,readonly);
```
### Revoke Permission

Remove permission for user to access a jaseci object
`obj` : target element
`element` : master to be revoke permission

**Return**
Sorted list

```jac
objects = std.revoke_perms(obj,element);
```

### Get Report

Get current report so far from walker run.

```jac
report = std.get_report();
```
