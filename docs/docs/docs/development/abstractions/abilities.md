---
sidebar_position: 3
description: An Overview of Abilities and Examples.
---

# Abilities

Nodes, edges, and walkers can have **abilities**. The body of an ability is specified with an
opening and closing braces ( `{` `}` ) within the specification of a node, edge, or walker and
specify a unit of execution.

Abilities are most closely analogous to methods in a traditional object oriented program,
however they do not have the same semantics of a traditional function. An ability can only
interact within the scope of context and local variables of the node/edge/walker for which it
is affixed and do not have a return semantic. (Though it is important to note, that abilities
can always access the scope of the executing walker using the visitor special variable as
described below)

When using abilities, a developer can think of these as self-contained in-memory/in-data
compute operations.

> **Note:**
>
> You can think of abilities as `methods` in traditional programming but however they are not similar in semantics;
> -   Abilities can be in nodes, edges or walkers
> -   Abilities cannot interact outside of the context and local variables of the attached node, edge, or walker, and does not have a return meaning.
>

To see node abilities in advance let's define the following graph, which represent cities and the connection between them.

![Abilities Graph Example](img/abilities_graph_example_1.png)

## Node Abilities Example

This is a very basic example of a node ability.

```jac
node city{
    has name;
    can set_name{ #also can use "with activity"
        name = "c1";
        std.out("Setting city name:", here.context);
    }
}

walker build_example{
    node1 = spawn here ++> node::city;
}

walker init{
    root{
        spawn here walker::build_example;
        take-->;
    }
    city{
        here::set_name;
        std.out(here.name);
    }
}
```

`set_name` is the ability defined inside the `city` node. This ability will set a name to the city node. `here::set_name` is the syntax of triggering the node ability from the `walker init`.

Expected output:

```
Setting city name: {"name": "c1"}
c1
```

The code defines a node called city which has a property called name and an ability called set_name. set_name sets the name property to "c1" and prints a message to the console using `std.out()`.

The code also defines a walker called build_example which spawns a new city node.

In the init walker, the root node spawns the build_example walker and then moves to the next node using take-->. The city node is the next node, and the walker triggers the set_name ability on this node using the syntax here::set_name. The std.out() function is then called to print the name property of the city node.

The output of this code is "Setting city name: {"name": "c1"} c1", which indicates that the set_name ability successfully set the name property to "c1" and printed the message to the console.


> **Note**
>
> To generate random integer values we can use `rand.integer` action from the rand action library;  `rand.integer(15,100)` will output a integer value between 15 and 100. More information about Jaseci standard actions can be found under the Jaseci [Actions](#actions) section;
>

The following jac program extends the above example to set tourists in each city nodes.

```jac
node city{
    has name;
    has tourists;

    can set_tourists{ #also can use "with activity"
        tourists = rand.integer(15,100);
        std.out("Setting number of tourists in", here.context.name,"city", "to",tourists);
    }
}

walker build_example{
    node1 = spawn here ++> node::city(name="c1");
    node2 = spawn node1 ++> node::city(name="c2");
    node3 = spawn node2 ++> node::city(name="c3");
    here ++> node2;
    node1 ++> node3;
}

walker init{

    root{
        spawn here walker::build_example;
        take-->;
    }

    city{
        here::set_tourists;
        take-->;
    }
}
```

`set_tourists` is the node ability in city node. `here::set_tourists` triggers the node ability inside the `init` walker.  To get the variable value from the current context `here.context.{variable_name}` has been used. Look at the `std.out` statement inside the `set_tourist` node ability. The node ability can also defined as `can set_tourists with activity {}`. The both definitions works similarly.

Run the example 2 code to obtain following output.

Expected output:

```
Setting number of tourists in c1 city to 47
Setting number of tourists in c2 city to 15
Setting number of tourists in c2 city to 69
Setting number of tourists in c3 city to 89
Setting number of tourists in c3 city to 51
Setting number of tourists in c3 city to 44
```
The `init` walker visits `c2` and `c3` edges multiple times as you can observe in the graph visualization `c2` and `c3` has multiple paths. to avoid resetting the number of tourists in each visit let's replace the `set_tourists` ability in the above example with following code snippet;

```jac
can set_tourists{ #also can use "with activity"
    if(here.tourists==null){
        tourists = rand.integer(15,100);
        std.out("Setting number of tourists in", here.context.name,"city", "to",tourists);
    }
}
```

In the following example adds another walker named `traveler`. To collect the value of a variable which is inside a walker we are using `visitor` keyword. See how it has been used inside the code snippet;

> **Note**
> `here` refers to the current node scope pertinent to the program's execution point and `visitor` refers to the pertinent walker scope pertinent to that particular point of execution. All variables, built-in characteristics, and operations of the linked object instance are fully accessible through these references. More information about here and visitor can be found in [here](#here-and-visitor)

A more advance example of node ability is discussed the below example;


```jac
node city{
    has name;
    has tourists;

    can set_tourists{ #also can use "with activity"
        if(here.tourists==null){
            tourists = rand.integer(15,100);
            std.out("Setting number of tourists in", here.context.name,"city", "to",tourists);
        }
    }

    can reset_tourists with traveler entry{
        here.tourists = here.tourists + visitor.tours;
        std.out("Total tourists in", here.context.name, "when traveler arrives:",here.tourists);
    }

}

walker build_example{
    node1 = spawn here ++> node::city(name="c1");
    node2 = spawn node1 ++> node::city(name="c2");
    node3 = spawn node2 ++> node::city(name="c3");
    here ++> node2;
    here ++> node3;
}

walker init{

    root{
        spawn here walker::build_example;
        take-->;
    }

    city{
        here::set_tourists;
        spawn here walker::traveler;
        take-->;
    }
}

walker traveler{
    has tours = 1;
}
```

Expected output:

```
Setting number of tourists in c1 city to 84
Total tourists in c1 when traveler arrives: 85
Setting number of tourists in c2 city to 74
Total tourists in c2 when traveler arrives: 75
Setting number of tourists in c3 city to 27
Total tourists in c3 when traveler arrives: 28
Total tourists in c2 when traveler arrives: 76
Total tourists in c3 when traveler arrives: 29
Total tourists in c3 when traveler arrives: 30
```

As you can see number of tourists has been increased by one in each city with `walker traveler` entry to each node.The code phrase `with traveler entry` instructs the node ability `reset_tourists` to only execute when the `traveler` walker enters the "city" node.

We can try resetting variable values inside a walker using a ability of a node on a visit. lets update the `walker traveler` and add `reset_walker_values` ability inside the `city` node to see if this works.

```jac
can reset_walker_value with traveler entry{
    visitor.walker_value =  1;
    std.out("Total visit of traveler is",visitor.walker_value);
}

walker traveler{
    has tours = 1;
    has walker_value = 0;
    std.out(walker_value);
}
```

You might observe that while using a node's ability, the walkers' state remains unchanged.

## Walker Abilities Example

Let's call a walker ability from a node in the following example;


```jac
node city{
    has name;
    has tourists;

    can set_tourists{ #also can use "with activity"
        if(here.tourists==null){
            tourists = rand.integer(15,100);
            std.out("Setting number of tourists in", here.context.name,"city", "to",tourists);
        }
    }
    can reset_tourists with traveler entry{
        here.tourists = here.tourists + visitor.tours;
        std.out("When traveler visits:",here.tourists, " tourists are in the city", here.context.name );
        visitor::print;
    }

}

walker build_example{
    node1 = spawn here ++> node::city(name="c1");
    node2 = spawn node1 ++> node::city(name="c2");
    node3 = spawn node2 ++> node::city(name="c3");
    here ++> node2;
    here ++> node3;
}

walker init{

    root{
        spawn here walker::build_example;
        take-->;
    }
    city{
        here::set_tourists;
        spawn here walker::traveler;
        take-->;
    }
}

walker traveler{
    has tours = 1;
    can print{
        std.out("Traveler enters the city");
    }
}
```

Expected output:

```
Setting number of tourists in c1 city to 33
When traveler visits: 34  tourists are in the city c1
Traveler enters the city
Setting number of tourists in c2 city to 99
When traveler visits: 100  tourists are in the city c2
Traveler enters the city
Setting number of tourists in c3 city to 16
When traveler visits: 17  tourists are in the city c3
Traveler enters the city
When traveler visits: 101  tourists are in the city c2
Traveler enters the city
When traveler visits: 18  tourists are in the city c3
Traveler enters the city
When traveler visits: 19  tourists are in the city c3
Traveler enters the city
```

Observe that the print statement "Traveler enters the city" comes from the `walker traveler` and triggers to executed when enters to a `city` node.

## Edge Abilities Example
<!-- Have to add an example here-->

## A Complete Example

Lets try adding following node ability inside city node;


```jac
can reset_tourists_1 with traveler exit{
    here.tourists = here.tourists - visitor.tours;
    std.out("When traveler leaves:",here.tourists, "tourists are in the city", here.context.name);
}
```

Expected output:

```
Setting number of tourists in c1 city to 76
When traveler visits: 77  tourists are in the city c1
When traveler leaves: 76 tourists are in the city c1
Setting number of tourists in c2 city to 84
When traveler visits: 85  tourists are in the city c2
When traveler leaves: 84 tourists are in the city c2
Setting number of tourists in c3 city to 60
When traveler visits: 61  tourists are in the city c3
When traveler leaves: 60 tourists are in the city c3
When traveler visits: 85  tourists are in the city c2
When traveler leaves: 84 tourists are in the city c2
When traveler visits: 61  tourists are in the city c3
When traveler leaves: 60 tourists are in the city c3
When traveler visits: 61  tourists are in the city c3
When traveler leaves: 60 tourists are in the city c3
```
`reset_tourists_1` executes when the `walker traveler` leaves the `city` node.

## Here and Visitor

At every execution point in a Jac/Jaseci program there are two scopes visible, that of the
walker, and that of the node it is executing on. These contexts can be referenced with the
special variables `here` and `visitor` respectively. Walkers use `here` to refer to the context of
the node it is currently executing on, and abilities can use `visitor` to refer to the context of
the current walker executing. Think of these are special `this` references.


```
node person {
    has name;
    has byear;

    #this sets the birth year from the setter
    can date.quantize_to_year::visitor.year::>byear with setter entry;

    #this executes upon exit of the walker from node
    can std.out::byear," from ", visitor.info:: with exit;

}

walker init {

    #collect the current time
    has year=std.time_now();
    root {
        person1 = spawn here ++> node::person(name="Josh", byear="1992-01-01");
        take --> ;
    }

    person {
        spawn here walker::setter;
    }
}

walker setter {
    has year="1995-01-01";
    }
```

Expected output:

```
1995-01-01T00:00:00  from  {"name": "setter", "kind": "walker", "jid": "urn:uuid:a3e5f4b6-aeda-4cd0-9552-506cb3b7c693", "j_timestamp": "2022-11-09T09:10:05.134836", "j_type": "walker", "context": {"year": "1995-01-01"}}
1995-01-01T00:00:00  from  {"name": "init", "kind": "walker", "jid": "urn:uuid:47f1e467-a0e6-4772-a06a-204f6a1b69c3", "j_timestamp": "2022-11-09T09:10:05.129720", "j_type": "walker", "context": {"year": "2022-11-09T09:10:05.131397"}}
```