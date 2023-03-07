# Nodes

In Jaseci, nodes are a crucial concept. There are two types of nodes:
- Root node: It is the starting point of the graph and is a built-in node type. Each graph can have only one root node.
- Generic node: It is a built-in node type that can be used throughout the Jaseci application. You can customize the name and properties of this node type as well.
Here's an example code snippet to create and spawn a node:

```jac
node person{
    has name, age, birthday, profession;
} 

walker init {
 person1 = spawn here node::person(name = "Josh", age = 32);
 person2 = spawn here node::person(name = "Jane", age = 30);

 std.out("Context for our people nodes");
 for i in -->{
    std.out(i.context);
 } 
 ```
}

# Node Abilities

Nodes in Jaseci can have abilities, which are self-contained in-memory/in-data compute operations. The body of an ability is specified within the specification of the node using opening and closing braces ( { } ).

Abilities in Jaseci are similar to methods in traditional object-oriented programming, but with some differences in their semantics. An ability can only interact with the context and local variables of the node it is affixed to and does not have a return semantic. However, it's worth noting that abilities can always access the scope of the executing walker using the special visitor variable.

Here's an example of a node with an ability:

```jac
node example_node {
    has name, count;

    can compute_sum {
        sum = 0;
        numbers = [1,2,3];
        for i in numbers{
            sum += i;
        }
        name = "Sum of first " + count.str + " numbers";
        report {"Computed sum: ": sum};
    }
}

walker init{
    spawn here ++>node::example_node;
    root{
        take-->[0];
    }
    example_node{
        here::compute_sum;
    }
}
```

In this example, compute_sum is an ability that computes the sum of the first count numbers and sets the name attribute to reflect the computation. The report statement is used to output the result of the computation during the execution of the walker.

Abilities can be a powerful tool for organizing and encapsulating logic within nodes in Jaseci.

