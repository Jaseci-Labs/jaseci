# Permission Management

This document provides a guide on managing graph-based access permissions on the cloud using a structure of architypes. Each user has their own root graph, and access between users' architypes is restricted by default.

# Anchors vs Architypes
- Architypes are Jaclang class representation
- Anchors are database class representation

| type | Anchors | Architypes |
| ---- | ---- | ---- |
| Node | NodeAnchor | NodeArchitype |
| Edge | EdgeAnchor | EdgeArchitype |
| Walker | WalkerAnchor | WalkerArchitype |
| Object | ObjectAnchor | ObjectArchitype |
| Root | NodeAnchor | Root(NodeArchitype) |
| GenericEdge | EdgeAnchor | GenericEdge(EdgeArchitype) |

```python
node Human {
    has gender: str;
}

# DB NodeAnchor Representation
{
    _id: ObjectId('6735b60656e82d6799dc9772'),
    name: 'Human',
    root: ObjectId('6735b5e456e82d6799dc976e'),
    access: { all: 'NO_ACCESS', roots: { anchors: {} } },
    edges: [ 'e::6735b60656e82d6799dc9775', 'e:Friend:6735b60656e82d6799dc9776' ],

    # the actual NodeArchitype and it's context or `has attributes`
    architype: {
        gender: "boy"
    },
}

edge Friend {
    has best: bool;
}

# DB EdgeAnchor Representation
{
    _id: ObjectId('6735b60656e82d6799dc9776'),
    name: 'Friend',
    root: ObjectId('6735b5e456e82d6799dc976e'),
    access: { all: 'NO_ACCESS', roots: { anchors: {} } },
    source: 'n:B:6735b60656e82d6799dc9771',
    target: 'n:C:6735b60656e82d6799dc9772',
    is_undirected: false

    # the actual EdgeArchitype and it's context or `has attributes`
    architype: {
        best: true
    },
  }
```

## Access Levels
* `NO_ACCESS`: No other user can access current architype.
* `READ`: Other user have Read-Only access to current architype.
* `CONNECT`: Other user's node can connect to current node.
* `WRITE`: Other user can do anything to current architype.

## Default User Graph Structure
In this setup, each user's architype (node, edge, walker) is isolated with default permissions as follows:
```python
{
    "all": "NO_ACCESS",
    "roots": {
        "anchors": {}
    }
}
```

* `all`: Non specific access (Given to all users)
* `roots`: Root specific access (specific to user)
    ```python
    "roots": {
        "anchors": {
            "{{root_jid}}": "NO_ACCESS"
        }
    }
    ```
## Access Level Prioritization
Specific root access will get prioritize over "all" access. This is to support different scenario such as:
 - all: `NO_ACCESS` roots: `root2: CoNNECT`
   - all user will have no access except user2 which will have connect access
 - all: `WRITE` roots: `root2: NO_ACCESS`
   - user2 will have no access while all other user have write access

## Example Structure in DB perspective
Consider the following structure:

```
User1 -> Root1 -> Node1
User2 -> Root2 -> Node2
```

By default, `User2` cannot access `Node1` owns by `Root1`. To allow `User2` access to `node1`, we need to explicitly add a permission mapping in `Root2`.

## Example of Granting Access
To grant `READ` access to `User2` for `Node1` owns by `Root1`, we modify Node1’s access permissions:
```python
# Node1 is the architype
# Node1.__jac__ is the anchor

Node1.__jac__.access = {
    "all": "READ",
    "roots": {
        "anchors": {}
    }
}
```
If `User1` wants to give only `READ` access to `User2`, we set permissions as follows:
```python
# Node1 is the architype
# Node1.__jac__ is the anchor

Node1.__jac__.access = {
    "all": "NO_ACCESS",
    "roots": {
        "anchors": {
            "n::123445673 User2's Root JID": "READ"
        }
    }
}
```

## Permission Management Walkers
Consider this scenario:
```python
User1 -> Root1 -> Node:boy1
User2 -> Root2 -> Node:boy2
User3 -> Root3 -> Node:boy3
```
### Granting Access

To grant `boy1` in `User1`’s graph access to `User2`, we can use a walker.
#### Granting Access in jac-lang
```python
# Run the walker in user1
walker set_access {
    has access: str;            # "READ", "WRITE", "CONNECT"
    has root_uuid: str;

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
    has access: str;            # "READ", "WRITE", "CONNECT"
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
            "n::123445673 User2's Root JID": "READ"
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
    has root_uuid: str;

    can remove_access with boy entry {
        # here = boy1
        Jac.disallow_root(here, UUID(self.root_uuid));
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
Jac.perm_grant(here, "READ")
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

## Manual Access Management

In some cases, you may need to manually verify, filter, or update access permissions on nodes. The following Python examples demonstrate how to handle these tasks.

### Checking Access Manually

To manually check access levels on a collection of nodes, you can use the following code. This script filters nodes by type and checks for `READ`, `WRITE`, and `CONNECT` access permissions.

```python
for nodeanchor in NodeArchitype.Collection.find(
    {
        "type": "<type of the node>",
        "context.public": true
    }
):
    # Check read access
    if not Jac.check_read_access(nodeanchor):
        continue

    # Check write access
    if not Jac.check_write_access(nodeanchor):
        continue

    # Check connect access
    if not Jac.check_connect_access(nodeanchor):
        continue
```

### Filtering Nodes by Type
To retrieve a specific node based on its type, use the following code snippet. This will find a node of the specified type that is also public in context.

```python
node = NodeArchitype.Collection.find_one(
    {
        "type": "<type of the node>",
        "context.public": true
    }
)
```

### Updating Access Permissions Manually
To manually update access permissions for multiple nodes, use the following code. This example sets the `access.all` permission to `CONNECT` for all nodes of a specific type that are publicly accessible.
```python
NodeArchitype.Collection.update_many(
    {
        "type": "<type of the node>",
        "context.public": true
    },
    {
        "$set": {
            "access.all": "CONNECT"
        }
    }
)
```

