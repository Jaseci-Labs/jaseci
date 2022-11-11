# Understanding Abilities by Example

You can think of abilities as `methods` in traditional programming but however they are not similar in semantics;
-   Abilities can be in nodes, edges or walkers
-   Abilities cannot interact outside of the context and local variables of the attached node, edge, or walker, and does not have a return meaning.

## Basic example of node abilities

This is a very basic example of a node ability.

**Example 1:**
```jac
node city{
    has name;
    can set_name{ #also can use "with activity"
        name = "c1";
        std.out("Setting city name:", here.context);
    }
} 

walker build_example{
    node1 = spawn here --> node::city;
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

**Output 1:**
```
Setting city name: {"name": "c1"}
c1
```

To see node abilities in advance let's define the following graph, which represent cities and connection between the them.

<div style="text-align:center"><img style="align:center" src="images/abilities_graph_example_1.png" /> <b>Example Graph</b></div>

> **Note**
> 
> To generate random interger values we can use `rand.integer` action from the rand action library;  `rand.integer(15,100)` will output a integer value between 15 and 100;
> 

The following example will set city names in each node;

**Example 2:**

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
    node1 = spawn here --> node::city(name="c1");
    node2 = spawn node1 --> node::city(name="c2");
    node3 = spawn node2 --> node::city(name="c3");
    here --> node2;
    node1 --> node3;
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

Run the example code to obtain following output.

**Output 2:**
```
Setting number of tourists in c1 city to 47
Setting number of tourists in c2 city to 15
Setting number of tourists in c2 city to 69
Setting number of tourists in c3 city to 89
Setting number of tourists in c3 city to 51
Setting number of tourists in c3 city to 44
```
The `init` walker visits `c2` and `c3` edges multiple times as you can observe in the graph visualization `c2` and `c3` has multiple paths. to avoid resettnig the number of tourists in each visit let's replace the `set_tourists` ability with following code snippet;

```jac
can set_tourists{ #also can use "with activity"
    if(here.tourists==null){
        tourists = rand.integer(15,100);
        std.out("Setting number of tourists in", here.context.name,"city", "to",tourists);
    }
}
```

## Basic example of walker abilities

In the following example adds another walker named `traveller`. To collect the value of a variable which is inside a walker we are using `visitor` keyword. See how it has been used inside the code snippet;

> **Note**
> `here` refers to the current node scope pertinent to the program's execution point and `visitor` refers to the pertinent walker scope pertinent to that particular point of execution. All variables, built-in characteristics, and operations of the linked object instance are fully accessible through these references.

**Example 3:**

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

    can reset_tourists with traveller entry{
        here.tourists = here.tourists + visitor.tours;
        std.out("Total tourists in", here.context.name, "when traveller arrives:",here.tourists);
    }

} 

walker build_example{
    node1 = spawn here --> node::city(name="c1");
    node2 = spawn node1 --> node::city(name="c2");
    node3 = spawn node2 --> node::city(name="c3");
    here --> node2;
    here --> node3;
}

walker init{

    root{
        spawn here walker::build_example;
        take-->;
    }

    city{
        here::set_tourists;
        spawn here walker::traveller;
        take-->;
    }
}

walker traveller{
    has tours = 1;
}
```
**Output 3:**

```
Setting number of tourists in c1 city to 84
Total tourists in c1 when traveller arrives: 85
Setting number of tourists in c2 city to 74
Total tourists in c2 when traveller arrives: 75
Setting number of tourists in c3 city to 27
Total tourists in c3 when traveller arrives: 28
Total tourists in c2 when traveller arrives: 76
Total tourists in c3 when traveller arrives: 29
Total tourists in c3 when traveller arrives: 30
```

As you can see number of tourists has been increased by one in each city with `walker traveller` entry to each node.The code phrase `with traveler entry` instructs the node ability `reset_tourists` to only execute when the `traveller` walker enters the "city" node.

We can try resetting variable values inside a walker using a ability of a node on a visit. lets update the `walker traveller` and add `reset_walker_values` ability inside the `city` node to see if this works.

```jac
can reset_walker_value with traveller entry{
    visitor.walker_value =  1;
    std.out("Total visit of traveller is",visitor.walker_value);
}

walker traveller{
    has tours = 1;
    has walker_value = 0;
    std.out(walker_value);
}
```

You might observe that while using a node's ability, the walkers' state remains unchanged. 

Let's call a walker ability from a node in the following example;

**Example 4:**

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
    node1 = spawn here --> node::city(name="c1");
    node2 = spawn node1 --> node::city(name="c2");
    node3 = spawn node2 --> node::city(name="c3");
    here --> node2;
    here --> node3;
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

**Output 4:**
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

Lets try adding following node ability inside city node;

**Example 5**

```jac
can reset_tourists_1 with traveler exit{
    here.tourists = here.tourists - visitor.tours;
    std.out("When traveler leaves:",here.tourists, "tourists are in the city", here.context.name);
}
```
**Output 5**
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
