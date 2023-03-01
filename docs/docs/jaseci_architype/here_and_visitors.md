# Understanding Contexts in Jaseci Programs

In Jaseci programming, two scopes are visible at every execution point: the walker's scope and the node's scope. These scopes can be referenced using the special variables "here" and "visitor," respectively. The walker uses "here" to refer to the context of the node it is currently executing on, while abilities use "visitor" to refer to the context of the current walker executing.

For example, let's say we have a Jaseci program that defines a "person" node with attributes such as "name," "age," and "profession." We also have a walker that iterates over all "person" nodes in the graph and prints out their names. We can access the "name" attribute of each node using the "here" context, like so:

```jac
node person {
    has name, age, profession;
}
edge society{
    has location;
}

graph  people_in_society{
    has anchor community;
    spawn{
        professions = ["lawyer", "doctor", "teacher", "athlete", "entrepreneur"];
        community = spawn node::person(name = rand.word(), age = rand.integer(34, 56), profession = rand.choice(professions));
        for i in professions{
            spawn community +[society]+> node::person(name = rand.word(), age = rand.integer(34, 56), profession = rand.choice(professions));
        }
    }
}
walker print_names {
    community = -[society]->;
    for persons in community{
        take -[society]->;
        std.out(here.name);
    }
}
 walker init{
    spawn here ++> graph::people_in_society;
    spawn here walker::print_names;
    root{
        take-->[0];
    }
 }
```