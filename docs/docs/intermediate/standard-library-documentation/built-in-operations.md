---
sidebar_position: 2
---

# Built in Operations

## Spawn

- Used to spawn/create walkers or nodes.
- Nodes can either be spawned with edges and types in a single spawn statement

**Spawning a node**

- Spawning generic code

```jac
node1 =  spawn node;
```

- spawning a typed node (of type person)

```jac
node1  = spawn node::person;
```

- spawning a node with edges
```jac
spawn node::person <--[friend]--> node::person;
# or #
node1 = spawn node::person;
node2 = spawn node::person;
node1 <-[friend]-> node2
```

- spawning a walker

```jac
spawn [name_of_walker];
```

## Has

- Nodes and Edges can be defined with various properties.
- The has keyword is used to defined these properties in the node/edge definition

**Defining a node with properties**

```jac
node [name_of_node]{
has parameter_1, parameter_2, parameter_n
}
```

## Can
- Nodes and Edges can be defined with various action that they can perform.
- The can keyword is used to defined these actions in the node/edge definition

- Actions can be seen as functions the node/edge has access to. Without declaring these actions, a node/edge cannot make use of them.

**Defining a node with actions**
```jac
node [name_of_node]{
can action_1, action_2, action_n
}
```

## Anchor

- The anchor keyword is used to tag a single property of a node/edge.
- The property that is tagged with the anchor keyword can be used as the return value of that node/edge.

**Making use of the anchor keyword**
```jac
node [name_of_node]{
has parameter_1, anchor parameter_2, parameter_n
}
```

### Take
- Take is used for node/edge traversal in a walker.
- It is asynchronous in nature and acts like a queue.
- Only until all other walker logic is executed, then all queued up take operations are executed.
- An operation would tell the walker to move/traverse on to the next node with the given filter provided when using take.
- When using the take command, you have the ability to filter by edges or edges that have a specific node attached.

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

**Traversing to a specific type of edge from a walker**

```jac
walker testWalker{
    node_type{
        take -[edge_type]->;
    }
}

//edge of type friend as the filter

walker testWalker2{
    person{
       take -[friend]->;
    }
}
```

**Traversing to a specific type of edge that has a specific type of node from a walker**

```jac
walker testWalker{
   node_type{
        take -[edge_type]-> node::node_type;
   }
}

//edge of type friend  and node person as the filter

walker testWalker2{
    person{
       take -[friend]-> node::person;
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

## Here

- here is the keyword used to make reference to / get context of the current node a walker is on.
- you can access the properties or actions of that node using here.
- you can also used it to spawn other nodes/walker from that code.

## Report

- report is an asynchronous operation that queues up data to be returned to the top level api call.
- It can be thought of as a global list that can be appended to by any walker through out the request.
- The data returned from using the report is always a list.

> One use case of this can be for instance, let's say you have walker, with the sole purpose of finding uncompleted tasks. When the walker begins traversing the graph, based on the logic, it can make use of the report command to add the uncompleted tasks to the global list. Then at the end of the traversal the list of uncompleted tasks is presented.

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

![Diagram of a road map](/img/tutorial/intermediate/take-5.png)

