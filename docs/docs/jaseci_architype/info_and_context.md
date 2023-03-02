# Info and Context Comand 

In our coding language, Jaseci, you can use the "info" and "context" commands to view the content of a node or edge. Although the following example demonstrates the use of these commands on nodes, the same principles can be applied to edges as well. Take a look at the example below to see how to use the "info" and "context" commands.

```jac
node example{
    has name = "Testing Info and Context commands";
    has result = "Success";
    has favourite_quote = "How you do anything is how you do everything therefore excellence auth to be an habit not an act";
}

walker init{
    example = spawn here node::example;
    context = example.context;
    info = example.info;
    std.out("This is the context result:", context);
    std.out("This is the info result:", info);
}
```

After executing the command above, you will observe that the context command displays variables such as name, result, and favourite quote, while the info command displays all the information related to the node.