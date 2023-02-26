## Skipping and Disengaging

Jac offers couple of more useful control statements that are pretty convenient, `skip` and `disengage`, with walker traversing graphs with `take` commands.

### Skipping

The idea behind the abstraction of `skip` in the context of a walkers code block is that it tells a walker to halt and abandon any unfinished work on the current node in favor of moving to the next node (or complete computation if no nodes are queued up).

> **Note**
>
> Node/edge abilities also support the usage of the skip directive. The skip merely decides not to use the remaining steps of that `ability` itself in this context.


Lets change the `init` walker of **Example 3** to demostrate how the `skip` command works;

**Example 5:**

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
        ## Skipping the nodes with even numbers
        if(here.number % 2==0): skip;
        std.out(here.number);
        take-->;
    }
}
```

**Output 5:**

```
1
5
7
```
Now it is evident when the node number is an even number, the code in the example above skips the code execution for the particular node. The line `if(here.number %2 ==): skip;` says walker to skips nodes with an even number.

The skip command "breaks" out of a walker or ability rather than a loop, but otherwise has semantics that are nearly comparable to the standard `break` command in other programming languages.

### Disengaging

The command `disengage` tells the walker to stop all execution and "disengage" from the graph (i.e., stop visiting nodes anymore from here) and can only be used inside the code body of a walker.

To demonstrate how the `disengage` command functions, let's once more utilize the `init` walker from example 3;

**Example 6:**

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

**Output 6**

```
1
2
```
The `init` walker in this example is nearly identical to the code in example 5, but we added the condition `if(here.numer == 5): disengage;`. This caused the walker to halt execution and finish its walk, thus truncating the output array.

>**Note**
>
> In addition to a standard disengage, Jac additionally supports a disengage-report shorthand of the type disengage report "I'm disengaging";. Before the disconnect really takes place, this directive produces a final report.

### Technical Semantics of Skip and Disengage

It's important to remember a few key semantic differences between `skip` and `disengage` commands.

    - The 'skip' statement can be used in the code bodies of walkers and abilities.
    - The 'disengage' statement can only be used in the code body of walkers.
    - 'skip' and 'disengage' statements have no effect on the block of code that ends with an 'exit'. Any code in a walker's with 'exit' block will start running as soon as the walker exit the graph.
    - An easy way to think about these semantics is as similar to the behavior of a traditional return (skip) and a return and stop walking (disengage).


## Ignoring and Deleting

The Jaseci walkers also have two more useful commands: `ignore` and `destroy`.

### Ignoring
The quite handy command `ignore` from Juseci allows you to skip(ignore) visiting nodes or edges when traversing.

**Example 7:**
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
    ignore -[family]->;
    ignore -[friend(name=="Dan")]->;
    take -->;
    }
person {
    std.out(here.name);
    take-->;
    }
}
```

### Deleting

To remove nodes or edges from the graph, Jaseci also offers the very useful command "destroy." Run the example that follows using the 'dot' command in the Jac shell. i.e. `jac dot main.jac`.

**Example 8:**

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
    for i in -[friend]->: destroy i;
    take -->;
    }

person {
    std.out(here.name);
    take-->;
}
}
```
The majic line in the above code is the `for i in -[friend]->: destroy i;` it instruct walker to remove all the nodes connected by friend edges. try playing with the code by removing and adding `destroy` command.


Graph before `destroy` command            |  Graph after `destroy` command
:-------------------------:|:-------------------------:
![Example Graph - Deleting 1](images/delete_example_before.png)  |  ![Example Graph 2 - Deleting 2](images/delete_example_after.png)


> **Note**
>
> To visualize the dot output can use the Graphviz. An online version of it is [Here](https://dreampuf.github.io/GraphvizOnline/).

## Yielding Walkers

In Jaseci, we have examined walkers that carry variables and state as they move around a graph. By default, a walker's state is cleared each time a walk is completed, but node/edge state is preserved. However, there are scenarios where you would want a walker to maintain its state across runs or even pause in the middle of a walk and wait to be explicitly called again, updating a subset of its dynamic state. This is where the yield keyword comes in.

To demonstrate the yield keyword, we will modify the 'init' walker from example 9.

Example 9:

**Example 9:**

```jac
.
.
.
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
        report here.context;
        take -->;
        yield;
    }
}
```
**Output 9:**
```json
{
  "success": true,
  "report": [
    {
      "name": "Joe"
    }
  ],
  "final_node": "urn:uuid:b7ebf434-bd90-443a-b8e2-c29589c3da57",
  "yielded": true
}
```

In this example, the yield keyword instructs the walker simple_yield to stop walking and wait to be called again, even though the walker is instructed to take--> edges. A single next node location is queued up, and the walker reports a single here.context each time it’s called, taking only 1 edge per call.

It's important to note that yield can be followed by a number of operations as a shorthand. For example, take-->; and yield; could be combined into a single line with yield take -->;. We call this a yield-take. Other shorthands include yield report "hi"; and yield disengage; and yield disengage report "bye";. In each of these cases, the take, report, and disengage operations execute with the yield.

### Technical Semantics of Yield

Yield has several key semantics that you should keep in mind, including:

1. When a yield is encountered, a report is returned and cleared.
2. Additional report items from further walking will be returned on subsequent yields or upon walk completion.
3. Similar to the take command, the entire walker body will execute on the current node and actually yield at the end of the execution. It is important to note that yield can be combined with disengage and skip commands.
4. If a prime node is supplied when continuing a walker after a yield, the walker will ignore the prime node and continue from where it left off on its journey if there are still other nodes to visit.
5. If there are no more nodes scheduled for the walker to visit, a prime node must be specified, or the walker will continue from the root by default.

6. Any entry or exit code blocks in the walker will not be executed when continuing from a yield or executing a yield, respectively. Regardless of how many yields there are in between, these blocks will only execute once at the beginning and end of the walk.
7. At the level of the master (user) abstraction, Jaseci maintains a distinction between walkers that have been yielded and need to be resumed and those that are currently being run. The semantics of walkers that are summoned as public are currently unclear. For customized yield behaviors, developers should use the more basic walker spawn and walker execute APIs.

### Walker Yielding Other Walkers

In addition to being useful when calling walkers from a client, the yield abstraction is also helpful when calling other walkers during a non-yielding walk. As shown in the figure, the walker "deep_yield" doesn't yield itself, but still enjoys the benefits of the yield command when calling the walker "simple_yield." Although deep_yield doesn't yield, it calls simple_yield 16 times and then exits. These 16 calls activate the walker simple_yield, which creates four connected nodes off of the root node and walks the chain one step at a time, yielding after each step. The result is a 17 node graph with a root node and three subtrees with four connected nodes each, showing the usefulness of the yield semantic.

```jac
walker simple_yield {
    with entry {
        t=here;
        for i=0 to i<4 by i+=1:
        t = spawn t ++> node::generic;
    }
    if(-->.length): yield take -->;
}

walker deep_yield {
    for i=0 to i<16 by i+=1 {
        spawn here walker::simple_yield;
    }
}
```