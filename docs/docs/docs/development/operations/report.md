---
sidebar_position: 8
---

# Report

The `report` command in jac resembles a conventional programming logging function in certain ways. The state of each node the walker visits while traversing continue to be recorded in this way.

```jac
node person: has name;
edge family;
edge friend;

walker build_example {
spawn here +[friend]+> node::person(name="Joe");
spawn here +[friend]+> node::person(name="Susan");
spawn here +[family]+> node::person(name="Matt");
spawn here +[family]+> node::person(name="Dan");
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
Expected Output:

```json
{
  "success": true,
  "report": [
    {
      "name": "person",
      "kind": "node",
      "jid": "urn:uuid:322c1695-172a-452a-8300-8000a793ad6c",
      "j_timestamp": "2023-05-04T03:29:35.258669",
      "j_type": "node",
      "context": {
        "name": "Joe"
      }
    },
    {
      "name": "person",
      "kind": "node",
      "jid": "urn:uuid:ca82f4a7-fd6b-4b15-bf82-58f620aa3920",
      "j_timestamp": "2023-05-04T03:29:35.258796",
      "j_type": "node",
      "context": {
        "name": "Susan"
      }
    },
    {
      "name": "person",
      "kind": "node",
      "jid": "urn:uuid:b44f0a68-3678-4de6-9638-75073c17eaf5",
      "j_timestamp": "2023-05-04T03:29:35.258899",
      "j_type": "node",
      "context": {
        "name": "Matt"
      }
    },
    {
      "name": "person",
      "kind": "node",
      "jid": "urn:uuid:80d723b1-a777-417c-a09d-deed9b356158",
      "j_timestamp": "2023-05-04T03:29:35.258994",
      "j_type": "node",
      "context": {
        "name": "Dan"
      }
    },
    {
      "name": "person",
      "kind": "node",
      "jid": "urn:uuid:9ac989c9-e123-4604-9566-4df8f9509c9a",
      "j_timestamp": "2023-05-04T03:29:35.259272",
      "j_type": "node",
      "context": {
        "name": "Joe"
      }
    },
    {
      "name": "person",
      "kind": "node",
      "jid": "urn:uuid:7b6589d0-25b2-4ffb-9941-9df503b4c6f9",
      "j_timestamp": "2023-05-04T03:29:35.259369",
      "j_type": "node",
      "context": {
        "name": "Susan"
      }
    },
    {
      "name": "person",
      "kind": "node",
      "jid": "urn:uuid:e6935002-7730-419e-ba9d-4f82667bd1d2",
      "j_timestamp": "2023-05-04T03:29:35.259464",
      "j_type": "node",
      "context": {
        "name": "Matt"
      }
    },
    {
      "name": "person",
      "kind": "node",
      "jid": "urn:uuid:d15b9cf8-5ab2-4121-95aa-e51eacdcc0e3",
      "j_timestamp": "2023-05-04T03:29:35.259557",
      "j_type": "node",
      "context": {
        "name": "Dan"
      }
    }
  ],
  "final_node": "urn:uuid:d15b9cf8-5ab2-4121-95aa-e51eacdcc0e3",
  "yielded": false
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