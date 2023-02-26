# Walker Spawning in Jaseci: Little Robots Walking Graphs

Jaseci walkers act like little robots traversing graphs, with a unique ability to spawn other walkers that can also walk the graph and return a value to the parent walker. This powerful feature is achieved by specifying the variable to receive the returned value using the "has anchor some_variable" syntax.

Here's a simple example of how to use walker spawning in Jaseci:

```jac
walker parent {
    has result;

    result = spawn here walker::child;

    std.out("Child walker returned: ", result);
}

walker child {
    has anchor return_value;

    return_value = "Hello, I am the child walker!";
}
```

In this example, the parent walker spawns the child walker and sets the return_value anchor to a string. The parent walker then assigns its result variable to the value returned by the child walker, and finally outputs the returned value using std.out.

With this feature, you can easily create dynamic traversal patterns that adapt to changing data and requirements, making Jaseci a powerful tool for developing complex applications.