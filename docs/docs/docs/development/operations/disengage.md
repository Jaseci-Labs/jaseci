---
sidebar_position: 5
---

# Disengage

The command `disengage` tells the walker to stop all execution and "disengage" from the graph (i.e., stop visiting nodes anymore from here) and can only be used inside the code body of a walker.

To demonstrate how the `disengage` command functions, let's once more utilize the `init` walker from [example](../abstractions/walkers.md#walkers-navigating-graphs-example);

**Example:**

```jac
.
.
.

#init walker traversing
walker init {
    root {
        start = spawn here ++> graph::example;
        take-->;
        }
    plain {
        ## Stoping execution from the node number equals to 5
        if(here.number==5): disengage;
        std.out(here.number);
        take-->;
    }
}
```

**Output:**

```
1
2
```
The `init` walker in this example is nearly identical to the code in example 5, but we added the condition `if(here.numer == 5): disengage;`. This caused the walker to halt execution and finish its walk, thus truncating the output array.

>**Note**
>
> In addition to a standard disengage, Jac additionally supports a disengage-report shorthand of the type disengage report "I'm disengaging";. Before the disconnect really takes place, this directive produces a final report.


**Technical Semantics of Skip and Disengage**

It's important to remember a few key semantic differences between `skip` and `disengage` commands.

    - The 'skip' statement can be used in the code bodies of walkers and abilities.
    - The 'disengage' statement can only be used in the code body of walkers.
    - 'skip' and 'disengage' statements have no effect on the block of code that ends with an 'exit'. Any code in a walker's with 'exit' block will start running as soon as the walker exit the graph.
    - An easy way to think about these semantics is as similar to the behavior of a traditional return (skip) and a return and stop walking (disengage).