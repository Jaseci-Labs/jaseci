# Title: Exploring Graphs with the Versatile Take Command in Jaseci

Jaseci's take command is a powerful tool that enables you to traverse graphs with ease. By default, it performs a breadth-first traversal, but you have the option to specify a different orientation, either breadth-first (:bfs) or depth-first (:dfs). Let's take a look at an example that demonstrates this feature.

Consider the following program, which defines a static three-level binary tree structure. We have two walkers, one using a breadth-first traversal and another using a depth-first traversal. The order of visited nodes is demonstrated by the print statement, and it corresponds to the specified traversal order. You can also use the shorthand :b or :d to specify breadth-first or depth-first traversals, respectively.

```jac
node plain: has name;

graph example {
    has anchor head;
    spawn {
        n=[];
        for i=0 to i<7 by i+=1 {
            n.l::append(spawn node::plain(name=i+1));
        }
        n[0] ++> n[1] ++> n[2];
        n[1] ++> n[3];
        n[0] ++> n[4] ++> n[5];
        n[4] ++> n[6];

        head=n[0];
    }
}

 walker walk_with_breadth {
    has anchor node_order = [];
    node_order.list::append(here.name);
    take:bfs ++>; #take:b can also be used
 }

 walker walk_with_depth {
    has anchor node_order = [];
    node_order.l::append(here.name);
    take:dfs -->; #take:d can also be used
}

walker init {
    start = spawn here ++> graph::example;
    b_order = spawn start walker::walk_with_breadth;
    d_order = spawn start walker::walk_with_depth;
    std.out("Walk with Breadth:",b_order,"Walk with Depth:",d_order);
}
```