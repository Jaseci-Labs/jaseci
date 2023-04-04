
Here's an example of an edge with an ability:

```jac
node person: has name;

 walker build_example {
    persons = ["Sally", "John", "Peter", "Mary", "Sarah"];
    for person in persons{
        spawn here +[person]+> node::person(name = person);
    }
}

edge person{
    has count = 0;

    can count_people{
        count += 1;
        connected_node = here.details["to_node_id"];
        person_name = (*connected_node).context["name"];
        std.log("I am person number: ", count, ". My name is: ", person_name);
    }
}

walker init{
    root{
        spawn here walker::build_example;
        persons = ["Sally", "John", "Peter", "Mary", "Sarah"];
        for i in -[person]->.edge{
            i::count_people;
        }
        disengage;
    }
}
```

In Jaseci, edge abilities execute only when explicitly called. If with entry or with exit is applied to an edge ability, it is essentially ignored. You can call it using something like -->.edge[0]::count_travelers.