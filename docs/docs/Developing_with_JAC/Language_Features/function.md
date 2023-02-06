---
title : Functions
---

Nodes and Walkers can have unique abilities. These are  much like functions. They can be executed in different scenarios.

## Nodes and Functions

The basic syntax for a function is as follows. Walkers can execute this code by simply using `here.[name of function] `

```jac
node [name of node ] {
    can [name of function] {

        # enter code to be executed here
    }
}
```

### Execute with entry and exit

Node functions can be executed when a walker traverses on to it or when a walker leaves
```jac
node [name of node ]  {
    can [name of function]entry  {

        # enter code to be executed when walker traverses on this node
    }

      can [name of function] exit {

        # enter code to be executed when walker leaves this node
    }
}

```

### Execute with sepcific walker

Nodes can have their functions only executed by a specific walker

```jac
node [name of node ] {
    can [name of function] with [namme of walker ] {

        # enter code to be executed here
    }
}
```

### Excute with specific walker on entry and exit

```jac
node [name of node ] {
    can [name of function] with [namme of walker ] entry {

        # enter code to be executed here
    }
      can [name of function] with [namme of walker ] exit{

        # enter code to be executed here
    }
}
```

