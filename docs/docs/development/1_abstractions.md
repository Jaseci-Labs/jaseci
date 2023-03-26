# Abstractions of Jaseci

There are a number of abstractions and concepts in Jac that is distinct from most (all?) other languages. These would be a good place to begin understanding for a seasoned / semi-seasoned programmer. In a nutshell...

- [Abstractions of Jaseci](#abstractions-of-jaseci)
  - [Graphs](#graphs)
    - [Nodes](#nodes)
    - [Edges](#edges)
    - [Examples](#examples)
  - [Walkers](#walkers)
    - [Examples](#examples-1)
      - [Basic Example](#basic-example)
      - [Walkers Navigating Graphs Example](#walkers-navigating-graphs-example)
  - [Abilities](#abilities)
    - [Examples](#examples-2)
  - [Actions](#actions)
    - [Examples](#examples-3)
  - [Here and Visitor](#here-and-visitor)
    - [Examples](#examples-4)

## Graphs

It is strange to see how our programming languages have evolved over the years, and yet, one fundamental data structure has been left behind. Almost every data structure used by programmers to solve problems can be represented as a graph or a special case of a graph, except for hash tables. This means that structures such as stacks, lists, queues, trees, heaps, and even graphs can be modeled with graphs. But, despite this, no programming language uses graph semantics as its first order data abstraction.

The graph semantic is incredibly rich and intuitive for humans to understand and is particularly well suited for conceptualizing and solving computational problems, especially in the field of AI. However, some may argue that there are graph libraries available in their preferred language and that a language forcing the concept is not necessary. To this, I argue that core design languages are based on their inherent abstractions, and with graphs not being one of them, the language is not optimized to allow programmers to easily utilize the rich semantics that graphs offer.

Another argument against using graphs as a first-order abstraction is that it might slow down the language. However, modern programming languages have absurd abstractions, such as dynamic typing, which have a higher runtime complexity than what would be needed to support graph semantics. Jaseci aims to revolutionize how we perceive data and memory by making graphs, with their intuitive and rich semantics, the foundational primitive for memory representation.

In Jaseci, we elect to assume the following semantics for the graphs in Jaseci:

1. Graphs are directed with a special case of a doubly directed edge
type which can be utilized practically as an undirected edge.
2. Both nodes and edges have their own distinct identities (i,e. an edge isn’t representable
as a pairing of two nodes). This point is important as both nodes and edges can have
contexts.
3. Multigraphs (i.e., parallel edges) are allowed, including self-loop edges.
4. Graphs are not required to be acyclic.
5. No hypergraphs, as I wouldn’t want Jaseci programmers heads to explode.

Refer to [Wikipedias description of graphs](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)) to learn more about graphs.

### Nodes


### Edges

In Jaseci, edges are an essential component of the graph structure, and they allow for more complex relationships between nodes. As stated above, just like nodes, you can define custom edge types with variables, allowing for more versatility in creating the structure of the graph.

Edges can have specific behaviors or conditions attached to them that trigger a specific action or behavior in the program. For example, in the custom edge provided above, the intent_transition edge type is defined to transition between states based on a user's input intent. This kind of edge behavior is incredibly useful in creating natural language processing (NLP) applications where the system must be able to understand and interpret user input.

By using custom edge types with specific behaviors, you can make your code more modular, easier to read and maintain, and add more functionality to your applications. Additionally, by using edges, you can create more complex relationships between nodes, which can be used to create more complex traversal patterns through the graph structure.

Overall, edges in Jaseci are a powerful tool that can be used to create more complex, intelligent, and versatile applications.


### Examples

```jac
edge name_of_edge{
    has name_of_variable;
}
```

## Walkers

One of the major innovations in Jaseci is the concept of walkers. This abstraction has never been seen in any programming language before and offers a new perspective on programmatic execution.

In a nutshell, a walker is a unit of execution that retains state (its local scope) as it travels
over a graphs. Walkers *walk* from node to node in the graph and executing its body.
The walker’s body is specified with an opening and closing braces ( `{` `}` ) and is executed to
completion on each node it lands on. In this sense a walker iterates while spooling through a
sequence of nodes that it ‘takes’ using the take keyword. We call each of these iterations
node-bound iterations.

Variables in a walker's body are divided into two categories: context variables, which retain their values as the walker moves through the graph, and local variables, which are reinitialized for each node-bound iteration.

Walkers offer a different approach to programmatic execution, distinct from the common function-based model used in other languages. Instead of a function's scope being temporarily pushed onto a growing stack as functions call other functions, scopes in Jaseci can be laid out spatially on a graph and walkers can traverse the graph, carrying their scope with them. This new model introduces data-spatial problem solving, where walkers can access any scope at any time in a modular manner, unlike in the function-based model where scopes become inaccessible after a function is called until it returns.

When solving problems with walkers, a developer can think of that walker as a little self-contained robot or agent that can retain context as it spacially moves about a graph, interacting with the context in nodes and edges of that graph.

### Examples

#### Basic Example

When we run a jac code, by default it's exucuting the `init` walker. Basically the `walker init` works as the main method in other programming language. save following code as `main.jac` and run the code in `jsctl` shell with `jac run main.jac`

**Example 1:**
```jac
walker init{
    std.out("This is from init walker \n");
}
```

**Output 1:**

```
    This is from init walker
```
As you can see, this code has executed the `init` walker. Now let's create another walker;


**Example 2:**
```jac
walker second_walker{
    std.out("This is from second walker \n");
}

walker init{
    std.out("This is from init walker");
    root{
        spawn here walker::second_walker;
    }
}

```

**Output 2:**
```
    This is from init walker
    This is from second walker
```

The statements from `second walker` and `init` are printed in the jac shell, and we may run just `second_walker` directly by using the command `jac run main.jac -walk second_walker`. Here, the `-walk` parameter instructs the `jsctl` to execute a certain walker.

#### Walkers Navigating Graphs Example

As mentioned earlier the walkers can traverse(walk) through the nodes of the graph in breadth first search (BFS) or depth first search(DFS) approaches.

> **Note**
>
> BFS is a traversal approach in which begins from root node and walk through all nodes on the same level before moving on to the next level. DFS is also a traversal approach in which the traverse begins at the root node and proceeds through the nodes as far as possible until we reach the node with no unvisited nearby nodes.

We are creating the following graph to demostrate traversing of walkers in comming sections;

 <div style="text-align:center"><img style="align:center" src="images/traverse_graph_example.PNG" /> <b>Example Graph - Navigating </b></div>

<p>
</p>

Jaseci introduces the handy command called "take" to instruct walker to navigate through nodes. See how that works in following example;

**Example 3:**
```jac
node plain: has number;

## defining the graph
graph example {
    has anchor head;
    spawn {
        n=[];
        for i=0 to i<7 by i+=1 {
            n.l::append(spawn node::plain(number=i+1));
        }

        n[0] --> n[1] --> n[2];
        n[1] --> n[3];
        n[0] --> n[4] --> n[5];
        n[4] --> n[6];
        head=n[0];
        }
    }

#init walker traversing
walker init {
    root {
        start = spawn here ++> graph::example;
        take-->;
        }
    plain {
        std.out(here.number);
        take-->;
    }
}
```

**Output 3:**
```
1
2
5
3
4
6
7
```
`take` command lets the walker travers through graph nodes. You may notice by default, a walker travers with `take` command using the breadth first search approach. But the `take` command is flexible hence you can indicate whether the take command should use a depth first or a breadth first traversal to navigate. Look at the following example; More information about `take` command and keywords to operate walkers can be found [here](2_operations.md#take)

## Abilities

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

### Examples


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

**Output 1:**
```
Setting city name: {"name": "c1"}
c1
```

To see node abilities in advance let's define the following graph, which represent cities and the connection between them.


The code defines a node called city which has a property called name and an ability called set_name. set_name sets the name property to "c1" and prints a message to the console using std.out().

The code also defines a walker called build_example which spawns a new city node.

In the init walker, the root node spawns the build_example walker and then moves to the next node using take-->. The city node is the next node, and the walker triggers the set_name ability on this node using the syntax here::set_name. The std.out() function is then called to print the name property of the city node.

The output of this code is "Setting city name: {"name": "c1"} c1", which indicates that the set_name ability successfully set the name property to "c1" and printed the message to the console.


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
    node1 = spawn here ++> node::city(name="c1");
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
    node1 = spawn here ++> node::city(name="c1");
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
    node1 = spawn here ++> node::city(name="c1");
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

## Actions

Actions enables bindings to functionality specified outside of Jac/Jaseci and behave as function
calls with returns. These are analogous to library calls in traditional languages. This external
functionality in practice takes the form of direct binding to python implementations that are
packaged up as a Jaseci action library.

> **Note**
>
> This action interface is the abstraction that allows Jaseci to do it's sophisticated serverless inter-machine optimizations, auto-scaling, auto-componentization etc.

### Examples

Jaseci has set of inbuilt actions. Also you can load and unload actions in `jsctl` shell. to see the available actions in jaseci session try running `actions list`. Here are two basic example of jaseci `date` actions.

**Example 1:**

```jac
node person {
    has name;
    has birthday;
}

walker init {
    can date.quantize_to_year;
    can date.quantize_to_month;
    can date.quantize_to_week;

    person1 = spawn here ++> node::person(name="Josh", birthday="1995-05-20");

    birthyear = date.quantize_to_year(person1.birthday);
    birthmonth = date.quantize_to_month(person1.birthday);
    birthweek = date.quantize_to_week(person1.birthday);

    std.out("Date ", person1.birthday);
    std.out("Quantized date to year ", birthyear);
    std.out("Quantized date to month ", birthmonth);
    std.out("Quantized date to week ", birthweek);
}
```
**Output 1:**
```
Date  1995-05-20
Quantized date to year  1995-01-01T00:00:00
Quantized date to month  1995-05-01T00:00:00
Quantized date to week  1995-05-15T00:00:00
```
The following example executes action in each person nodes of the graph.

**Example 2:**
```jac
node person {
    has name;
    has birthday;
}

walker init {
    can date.quantize_to_year;

    root {
        person1 = spawn here ++> node::person(name="Josh", birthday="1995-05-20");
        person2 = spawn here ++> node::person(name="Joe", birthday="1998-04-23");
        person3 = spawn here ++> node::person(name="Jack", birthday="1997-03-12");
        take -->;
    }

    person {
        birthyear = date.quantize_to_year(here.birthday);
        std.out(here.name," Birthdate Quantized to year ",birthyear);
        }
}
```

**Output 2:**
```
Josh  Birthdate Quantized to year  1995-01-01T00:00:00
Joe  Birthdate Quantized to year  1998-01-01T00:00:00
Jack  Birthdate Quantized to year  1997-01-01T00:00:00
```

## Here and Visitor

At every execution point in a Jac/Jaseci program there are two scopes visible, that of the
walker, and that of the node it is executing on. These contexts can be referenced with the
special variables `here` and `visitor` respectively. Walkers use `here` to refer to the context of
the node it is currently executing on, and abilities can use `visitor` to refer to the context of
the current walker executing. Think of these are special `this` references.

### Examples

**Example:**
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

**Output:**
```
1995-01-01T00:00:00  from  {"name": "setter", "kind": "walker", "jid": "urn:uuid:a3e5f4b6-aeda-4cd0-9552-506cb3b7c693", "j_timestamp": "2022-11-09T09:10:05.134836", "j_type": "walker", "context": {"year": "1995-01-01"}}
1995-01-01T00:00:00  from  {"name": "init", "kind": "walker", "jid": "urn:uuid:47f1e467-a0e6-4772-a06a-204f6a1b69c3", "j_timestamp": "2022-11-09T09:10:05.129720", "j_type": "walker", "context": {"year": "2022-11-09T09:10:05.131397"}}
```

