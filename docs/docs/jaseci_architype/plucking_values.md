# Plucking values from nodes and edges

In Jaseci, you can easily extract information from nodes and edges by using the pluck feature. Edges in Jaseci have a unique feature that allows you to pluck values from neighboring nodes and edges themselves. By using the syntax **-->**, you can extract the value of a specific variable from a neighboring node. This will return a list of the values of that variable from all connected nodes. If you want to filter the results and only extract information from specific nodes, you can specify the name of the edge connected to the node and further specify what value the edge has by using the syntax **-[name_of_edge(variable = value)]->.name_of_variable_needed**.

To pluck values from edges, you can simply use the syntax **-->** and specify the edge and variable name like this: **--> .edge.name_of_variable_needed**.

Here is an example of plucking values from nodes and edges in Jaseci:

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
            spawn community +[society(location = rand.word())]+> node::person(name = rand.word(), age = rand.integer(34, 56), profession = rand.choice(professions));
        }
    }
}
walker print_names {
    community = -[society]->;
    people = -[society]->.name;
    report {"Plucking people from edge": people};
    location = -[society]->.edge.location;
    report {"Plucking location from edges": location};
}

walker init{
    spawn here ++> graph::people_in_society;
    spawn here walker::print_names;
    root{
        take-->[0];
    }
}
 ```

 In this example, we create a graph called people_in_society that contains nodes representing people and an edge called society that connects the nodes. The society edge has a location variable. The print_names walker plucks the names of the people and their locations from the society edge and reports them.

The pluck feature in Jaseci allows for easy extraction of information from nodes and edges, which can be useful in many different scenarios.