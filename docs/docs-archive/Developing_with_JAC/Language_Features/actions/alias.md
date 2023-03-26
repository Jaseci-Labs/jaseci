# Alias Actions
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