# Permission Management

This document provides a guide on managing graph-based access permissions on the cloud using a structure of nodes and anchors. Each user has their own root graph, and access between users' graphs is restricted by default.

## Default User Graph Structure
In this setup, each user's graph is isolated with default permissions as follows:
```python
{
    "all": "NO_ACCESS",
    "roots": {
        "anchors": {}
    }
}
```

* `all`: Controls access to all archetypes (`nodes`, `edges`, and `walkers`).
    * If set to `NO_ACCESS`, other users cannot access any part of this user's graph.

## Example Structure
Consider the following structure:


```
user1 -> Root1 (NodeAnchor equivalent to NodeArchitype in jac laguage level) -> node1

user2 -> Root2 -> node2
```

By default, `user2` cannot access `node1` in `Root1`. To allow `user2` access to `node1`, we need to explicitly add a permission mapping in `Root2`.

## Access Levels
* `NO_ACCESS`: No access to nodes, edges or walkers.

* `READ`: Read-only access to nodes, edges and walkers.

* `CONNECT`: Can connect nodes using edges.

* `WRITE`: Can modify nodes, edges and walkers.

* `DELETE`: Can delete nodes and edges.

## Example of Granting Access
To grant `READ` access to `user2` for `node1` in `Root1`, we modify node1’s access permissions:
```python
node1.access = {
    "all": "READ",
    "roots": {
        "anchors": {}
    }
}
```
If `user1` wants to give only `READ` access to `user2`, we set permissions as follows:
```python
node1.access = {
    "all": "NO_ACCESS",
    "roots": {
        "anchors": {
            "roots": {
                "n::123445673 user2": "READ"
            }
        }
    }
}
```

## Permission Management Walkers
Consider this scenario:
```python
user1 -> Root1 -> node:boy:boy1
user2 -> Root2 -> node:boy:boy2
user3 -> Root3 -> node:boy:boy3
```
### Granting Access 

To grant `boy1` in `user1`’s graph access to `user2`, we can use a walker.
#### Granting Access in jac-lang
```python
# Run the walker in user1
walker set_access {
    has access: str;            # "READ", "WRITE", "CONNECT", "DELETE"
    has root_ref_jid: str;

    can give_access with boy entry {
        # here = boy1
        Jac.allow_root(here, UUID(self.root_ref_jid), self.access);       
    }
}
```

#### Granting Access in jac-cloud
```python
# Run the walker in user1
walker set_access {
    has access: str;            # "READ", "WRITE", "CONNECT", "DELETE"
    has root_ref_jid: str;

    can give_access with boy entry {
        # here = boy1
        Jac.allow_root(here, NodeAnchor.ref(self.root_ref_jid), self.access);      
    }
}
```
This is equivalent to setting boy1’s access in database:
```python
boy1.access = {
    "all": "NO_ACCESS",
    "roots": {
        "anchors": {
            "roots": {
                "n::123445673 user2": "READ"
            }
        }
    }
}
```
## Removing Access
To remove access, use the walker below.

#### Removing Access in jac-lang
```python
# Run the walker in user1
walker remove_access {
    has root_ref_jid: str;

    can remove_access with boy entry {
        # here = boy1
        Jac.disallow_root(here, UUID(self.root_ref_jid));     
    }
}
```
#### Removing Access in jac-cloud
```python
# Run the walker in user1
walker remove_access {
    has root_ref_jid: str;

    can remove_access with boy entry {
        # here = boy1
        Jac.disallow_root(here, NodeAnchor.ref(self.root_ref_jid));     
    }
}
```
This is equivalent to resetting boy1’s access:
```python
boy1.access = {
    "all": "NO_ACCESS",
    "roots": {
        "anchors": {}
    }
}
```

## Global Access Control
To grant read access to all, use the following syntax:
```python
Jac.unrestrict(here, "READ")
```
Equivalent structure:
```python
{
    "all": "READ",
    "roots": {
        "anchors": {}
    }
}
```

To remove access to all, use the following syntax:
```python
Jac.restrict(here)
```
Equivalent structure:
```python
{
    "all": "NO_ACCESS",
    "roots": {
        "anchors": {}
    }
}
```