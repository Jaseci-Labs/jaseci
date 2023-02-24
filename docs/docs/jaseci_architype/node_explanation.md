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

