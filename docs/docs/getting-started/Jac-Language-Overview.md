---
sidebar_position: 5
---

# JAC Language Overview

## How a JAC programs runs

The JAC Promgrammming language builds its paradigm on traversal of Graphs. The Walker is used to traverse graphs . The graph is a combination of nodes and edges connected together. We create our graphs and walkers and specify their abilities.

All traversal begins at the Init or default node. This `init` node will connect to the main root of our graph.


![Pic of Main Root](/img/tutorial/intermediate/root.png)

The Walkers are initialized and added on the root node and from there they begin traveral.
The walkers decide which node to travel to based on which edge satisfies it's intent. The intent being a criteria meet by the edge.

![Pic of Nodes and Edges](/img/tutorial/intermediate/graph.png) 

The Walker can move from node to node but it can also jump to other nodes that are not in it's path or connected directly in the path.



## Common Code Elements in Jaseci


 Jaseci supports many common code constructs.

### The select statement

```jac
# simple If statement
walker init {
    x = 3.56;
    y = "X is not equal to 3.45";

    if (x ==3.45) {
        std.out(x);
    }
    elif (x==3.56){
        std.out("it's a match");
    }
     else {
        std.out(y);
    }
}

```
Other Conditional statements like < , > ,!= , and and or are all supported.

### Loops

```jac
walker init {
    # the for loop
    for i=0 to i<10 by i+=1:
        std.out(i)

    #the while loop
    while(x<10){
        std.out(x);
        x = x +1;
    }
}
```

## Modelling structures with Nodes , Edges and Graphs

Nodes , Edges and Graphs are vital to any Jaseci program. 

### Nodes
A node is a representation of an entity.

* Nodes are composed of Context and excetuable actions.
* Nodes accumulate context via a push function, context can be read ass well
* Nodes can execute a set of actions upon entry and exit.

```jac 
node [name of node]{
    # to declare a variable
    has variable;
    # to use a module from jaseci kit
    can use_qa;
}
```

### Edges
* can be thought of as a relationship between nodes.
* Edges accumulate context via a push function , context can be read as well.
* Edges execute a set of actions when traversed.

```jac
edge [name of edge] {
    has variable;
}
```

### Graphs
* can be thought as the collections of nodes
* Within the Graph is where we link nodes and edges together to create conversational flows.

```jac
graph [name of graph] {
    this is the root node of the graph
    has anchor [name of anchor];

    #here is where we start to connect nodes with edges creating a graph.
    spawn{
        # declare your nodes in here 

     }
}
```

## Modelling Behaivours with Walkers.


### Walkers

* Walkers traverse nodes triggering execution at the node level.

* Walkers have the ability to pick upand retain context, which can be taken across nodes.

* Walkers also decides which node to travel to through next and records the path of travel to b recorded within it's own context.
* Walkers can be spawned at any node
* Walker can spawn other walkers.
* Walkers can carry with them their own actions and contexts that is executed whenever specified in the walkers own code

#### Defining a Walker

```jac 
 walker [name_of_walker]{

}
```
Defining specific node code to execute When defining a walker, you also write specific code blocks that will only execute when the walker is on a specific node.

```jac
 walker [name_of_walker]{
    [Any code here is executed regardless of the node the walker is on]
    ...
    ...

    person{
     [Any code within this block will only be executed when the walker is on a person node]
   }

   ...

   family{
    [Any code within this block will only be executed when the walker is on a family node]
   }

}
```
## More on Behaivour with Abilities 

#### With Entry and Exit 

When defining a walker, you also have the ability to write specific code blocks that execute if and only if a walker enters or exists a node. Any code within the with_entry block is the first thing that executes as soon as a walker enter a node. And the opposite is true for with_exit, triggering only when the walker is about to leave a node.

```jac 
walker [name_of_walker]{
    with entry{
        [code to execute when a walker first enters a node]
    }
    ...
    ...

    with exit{
        [code to execute when a walker is about to leave a node]
    }
}

```


## Specifying Operating Context

The Graph can several types of nodes and these nodes can have their own unique abilities.Walkers can be written to perform specific actions when it on a specific node. Call functions or attributes for the node it is on top.
```jac
node state {
    has title;
    has message;
    has prompts;
}

node input_state:state {
    has input;
}

node closing_state:state;

edge transition {
    has intent;
}

walker talker {

state, input_state{

    #execute code specific to the state and input_state nodes

    input_state{

        #These operating context can be embedded within other operating context.
        
    }

}

closing_state{
 
    #execute code specific to  closing_state nodes

}

}

```
 


## Passing Arguments to Walkers , Nodes and Edges

You can pass arguments to walkers , Nodes and Edges similarily to when passing arguments to functions in python.

### Passing Arguments to Walkers

```jac
walker talker {
    has name;
    has value;

}

spawn::talker(name="Jaseci" ,value = 10);
```

### Passing Arguments to Nodes
```jac 
node::calculator(first_number, second_number);
```

### Passing arguments to Edges
```jac
# edge named transittion with argument orperation
[transition(operation)]-> node ;
```





## Grabbing Results from reports 
* It can be thought of as a global list that can be appended to by any walker through out the request.
* The data returned from using the report is always a list.

```jac
node task{
    has anchor name, isCompleted;
}

walker myWalker{
    task{
        if(here.isCompleted){
            std.out('Completed');
        }else{
           std.out('not completed');
           report here;
        }
        take -->;

    }
}
```

## Walker - Node communication (visitor , here)

The `here` keyword is used reference the node the walker is currently on.

```jac 
walker talker {
    has utterance;

    state {
        #the message and prompts attribute of the current node will be printed
        std.out(here.message, here.prompts);

        utterance = std.input("> ");

        if(utterance == "quit"): disengage;

        take -[transition(intent == utterance)]-> node::state else {
            take here;
        }
    }
}

```
The `visitor` keyword is used to reference attributes of the walker from the node it is currently on.

```jac
node state{
    has prev_value;

    can getvalue with talker entry {
        here.prev_value = visitor.value;
        std.out(here.prev_value);
    }
}

## Telling Walkers where to walk (Take)


* Take is used for nodes/Edge trversal in a walker 

* Only until all other walker logic is executed, then all queued up take operations are executed.
* An operation would tell the walker to move/traverse on to the next node with the given filter provided when using take.
* When using the take command, you have the ability to filter by edges or edges that have a specific node attached.


Consider the following diagram

![Diagram of a road map](/img/tutorial/intermediate/take.png)

The take command performs a breath first search to add take operations to the queue. Let's define a walker that traverses the various nodes and prints the node data. We'll assume this walker spawns and starts from the root `node 0`.

**Traversing to a generic node from a walker**

```jac
// generic definition of the nodes. Nodes of type 'myNode' will have a 'data' property

node myNode: has anchor data;

walker myWalker{
    myNode{
        take -->;
        std.out(here.data);
    }
}
```

With the assumption that this walker starts from `node 0`, this is how the take operations are queued and executed.

![Diagram of a road map](/img/tutorial/intermediate/take-2.png)

Upon spawning, the walker executes whatever logic it has to when on node of type myNode and in the logic of the above code snippet, the walker executes a take operation then prints the node data.

However, due to the way the take command works, the data is first printed before any traversal occurs. This is becasue the take command is asynchronous and doesn't execute right away. Instead, it queues up any traversal that needs to occur, executes any logic that come after the take command and once that is complete, dequeues and executes the next operation, which would be the traversal to node1.

![Diagram of a road map](/img/tutorial/intermediate/take-3.png)

At node 1 the walker executes a similar logic, queuing up nodes 3 and 4 then printing the value of node 1 before any traversal. Once that logic is finished, it checks the end of the queue for the next operation, which in this case would be traversal to node 2.

![Diagram of a road map](/img/tutorial/intermediate/take-4.png)

This process continues until the queue is empty or the walker is killed.

**Basic traversal using take**

```jac
walker testWalker{
    node_type{
        take -->;
    }
}

 walker testWalker2{
    node_type{
        take <--;
    }
}
```

**Traversing to a specific type of node from a walker**

```jac
walker testWalker{
    node_type{
        take --> node::node_type;
    }
}

//node of type person as the filter

walker testWalker2{
    school{
        take --> node::person;
    }
}
```

Take also allows the use of an else statement, should there be no edges with the filter specified in the take command.

**Executing alternative logic should there be no edges with the take filter**

```jac
walker testWalker{
    node_type{
        take [some filter] else {

            // some additional logic if edge of filter not found
        }
    }
}

//traverse to friend edge, else print 'no friends found'

walker testWalker2{
    person{
        take -[friend]-> else{;
            std.out('no friends found');
        }
    }
}
```


