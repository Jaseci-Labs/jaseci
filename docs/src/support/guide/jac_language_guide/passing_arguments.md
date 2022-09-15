# Passing Arguments

You can pass arguments to walkers , Nodes and Edges, in a similar way as passing arguments to functions in python.

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


