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
```json
Setting city name: {"name": "c1"}
c1
```

To see node abilities in advance let's define the following graph, which represent cities and connection between the them.

<div style="text-align:center"><img style="align:center" src="images/abilities_graph_example_1.png" /> <b>Example Graph</b></div>

> **Note**
> 
> To generate random interger values we can use `rand.integer` action from the rand action library; This will output a integer value between 15 and 100;
> 

The following example will set city names in each node;
**Example 2:**

```jac
node city{
    has name;
    has tourists;

    can set_tourists{ #also can use "with activity"
        tourists = rand.integer(15,100);
        std.out("Setting number of tourists in", here.context.name,"city");
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
        std.out(here.tourists);
        take-->;
    }
}
```

`set_tourists` is the node ability in city node. `here::set_tourists` triggers the node ability inside the `init` walker.  Also you can see to get the variable value from the current context `here.context.{variable_name}` has been used. Look at the `std.out` statement inside the `set_tourist` node ability.

Run the example code to obtain following output.

**Output 2:**
```json
Setting number of tourists in c1 city
41
Setting number of tourists in c2 city
55
Setting number of tourists in c3 city
22
Setting number of tourists in c2 city
89
Setting number of tourists in c3 city
84
Setting number of tourists in c3 city
60
```
## Basic example of walker abilities

In the following example we are adding another walker called `traveller`. To collect the value of a variable which is inside a walker we are using `visitor` keyword. See how it has been used inside the code snippet;

**Example 3:**

```jac
node city{
    has name;
    has tourists;

    can set_tourists{ #also can use "with activity"
        tourists = rand.integer(15,100);
        std.out("setting number of tourists in", here.context.name,"city");
    }

    can reset_tourists with traveller entry{
        here.tourists = here.tourists + visitor.tours;
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
        std.out("Initial tourists :",here.tourists);
        spawn here walker::traveller;
        std.out("After traveller :",here.tourists);
        take-->;
    }
}

walker traveller{
    has tours = 1;
}
```
**Output 3:**

```json
Setting number of tourists in c1 city
Initial tourists : 90
After traveller : 91
Setting number of tourists in c2 city
Initial tourists : 73
After traveller : 74
Setting number of tourists in c3 city
Initial tourists : 20
After traveller : 21
Setting number of tourists in c2 city
Initial tourists : 19
After traveller : 20
Setting number of tourists in c3 city
Initial tourists : 78
After traveller : 79
Setting number of tourists in c3 city
Initial tourists : 82
After traveller : 83
```

As you can see number of tourists has been increased by one in each city with `walker traveller` entry to each node. Let's call a walker ability from a node in the following example;

**Example 4:**

```jac
node city{
    has name;
    has tourists;

    can set_tourists{ #also can use "with activity"
        tourists = rand.integer(15,100);
        std.out("setting number of tourists in", here.context.name,"city");
    }

    can reset_tourists with traveller entry{
        here.tourists = here.tourists + visitor.tours;
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
        std.out("Initial tourists :",here.tourists);
        spawn here walker::traveller;
        std.out("After traveller :",here.tourists);
        take-->;
    }
}

walker traveller{
    has tours = 1;

    can print{
        std.out("Traveller enters the city");
    }
}
```

**Output 4:**
```
setting number of tourists in c1 city
Initial tourists : 78
Traveller enters the city
After traveller : 79
setting number of tourists in c2 city
Initial tourists : 26
Traveller enters the city
After traveller : 27
setting number of tourists in c3 city
Initial tourists : 39
Traveller enters the city
After traveller : 40
setting number of tourists in c2 city
Initial tourists : 66
Traveller enters the city
After traveller : 67
setting number of tourists in c3 city
Initial tourists : 46
Traveller enters the city
After traveller : 47
setting number of tourists in c3 city
Initial tourists : 79
Traveller enters the city
After traveller : 80
```