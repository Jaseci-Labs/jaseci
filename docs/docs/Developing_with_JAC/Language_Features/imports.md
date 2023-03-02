# Jaseci: Working with Imports

One of the most important aspects of any coding language is the ability to efficiently organize code and build programs. In Jaseci, we use imports to make this process as simple and intuitive as possible.

## Importing Files

In Jaseci, you can easily import entire files using the following syntax:

```jac
import {*} with "path_to_file"
```

For example, to import an entire file called conv_walkers.jac, you would use:

```jac
import {*} with "./conv_walkers.jac"
```

This will import all of the graphs, nodes, and walkers contained in the specified file.

## Importing Specific Parts of a File

If you only need to import specific parts of a file, you can use the following syntax:

```jac
// import {feature::name, feature::{name, name}} with "path_to_file"
// you can replace features with abstractions like nodes, edges, graphs and walkers
// replace name with the name of the abstraction in your file
import {graph::dummy, node::{banana, apple}} with "path_to_file"
```
In this example, we are importing the dummy graph, as well as the banana, and apple nodes from the file located at path_to_file.

You can specify which types of objects you want to import (graphs, nodes, or walkers) by replacing graph in the above example with either node or walker.

## Example 

```jac
 import {graph::dummy, node::{banana, apple, testnode}} with "./jac_tests.jac";
 import {*} with "./jac_tests.jac";
 import {graph::dummy, node*} with "./jac_tests.jac";

 walker init {
    has num=4;
    with entry {
        spawn here ++> graph::dummy;
    }
    report here.context;
    report num;
    take -->;
}
```
**Output**
```
{
    "success": true,
    "report": [
        {},
        4,
        {
            "yo": "Hey yo!",
            "bro": null
        },
        4,
        {
            "x1": "I'm banana",
            "x2": null
        },
        4
    ]
}
```