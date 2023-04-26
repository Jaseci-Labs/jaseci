---
sidebar_position: 8
---

# Report

The `report` command in jac resembles a conventional programming logging function in certain ways. The state of each node the walker visits while trarsing will continue to be recorded in this way.

**Example:**
```jac
node person: has name;
edge family;
edge friend;

walker build_example {
spawn here -[friend]-> node::person(name="Joe");
spawn here -[friend]-> node::person(name="Susan");
spawn here -[family]-> node::person(name="Matt");
spawn here -[family]-> node::person(name="Dan");
}

walker init {
    root {
        spawn here walker::build_example;
        spawn -->[0] walker::build_example;
        take -->;
    }
person {
        report here; # report print back on disengage
        take -->;
    }
}
```
**Output:**
```json
{
  "success": true,
    {
      "name": "person",
      "kind": "node",
      "jid": "urn:uuid:dcec06b4-4b7f-461d-bbe1-1fbe22a0ed0c",
      "j_timestamp": "2022-11-03T10:18:08.328560",
      "j_type": "node",
      "context": {
        "name": "Matt"
      }
    },
    {
      "name": "person",
      "kind": "node",
      "jid": "urn:uuid:1dde2125-f858-401e-b0e8-fc2bdb7b38fb",
      "j_timestamp": "2022-11-03T10:18:08.330218",
      "j_type": "node",
      "context": {
        "name": "Dan"
      }
    }
}
```
A portion of the final result is shown in the sample above. As the number of nodes in the graphs grows, the output will lengthen.

**Report Custom**
Supports custom structure as response body.

Example:

```js
    report:custom = `{{ any | {} | [] }}`
```

**Usage**
This can be combine with walker_callback as 3rd party service requires different json structure on response.
It can also be used for different scenario that doesn't require ctx structure