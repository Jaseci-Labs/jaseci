---
sidebar_position: 4
---

# Write your first app

Let's create a simple conversational Agent using Jaseci and Jaseci Kit. We're gonna create a Chatbot for students to sign up for Jaseci Dojo !

Before we begin ensure you have Jaseci and Jaseci Kit installed. If not, see the Installation [here](installation)

Create a file called graph.jac. Here we are going to create the conversational flow for the chatbot .

```jac

# state is the name of the node
node state {
    has title;
    has message;
    has prompts;
}

```
Nodes can be thought of as the representation of an entity.
Nodes are the fundamental unit of  a gaph. These can be considered to be the steps in which the Walker can take.
* Nodes are composed of Context and excutable actions.
* Nodes execute a set of actions upon entry and exit.
 Here we are creating a `node` of name "state"
The <strong>has</strong> keyword is used to declare a variable of the node.

```jac

# state is the name of this node
node state {
    has title;
    has message;
    has prompts;
}

# transition is the name of this edge
edge transition {
    has intent;
}
```

Edges are the link between nodes. They walker will use these edges to determine the next node to traverse to.
The <strong>has</strong> key word is used to declare the variable "intent". This "intent" is what the Walker will use to to determine which node to go to next.

```jac

# state is the name of this node
node state {
    has title;
    has message;
    has prompts;
}
# transition is the name of this edge
edge transition {
    has intent;
}

# main_graph is name of the graph
graph main_graph {

    has anchor main_root

```

The `graph` is a collection of initialized nodes. 
The `has anchor` key word is used to identify the root node. The Root node is the node where the walker's traversal begins.
The <strong>has anchor</strong> key word is used to state the root node. The Root node is the node where the walker's traversal begins.


```jac
# state is the name of this node
node state {
    has title;
    has message;
    has prompts;
}

edge transition {
    has intent;
}
graph main_graph {

    has anchor main_root

spawn {
     # this is the first node in the graph.
     main_root = spawn node::state(
        title = "Welcome",
        message = "Welcome to Jaseci Dojo, how can i help?",
        prompts = ["class","times","prices","quit"]
    );


    # this creates a node that goes from main_root to class.
    prices = spawn main_root -[transition(intent="prices")] -> node::state(
        title = "prices",
        message = "Prices Vary based on age",
        prompts = ["12 and younger", "18 and younger" ,"Older than 18", "quit"]
    );

    # this creates a node from the prices node to here.
     prices_12 = spawn prices -[transition(intent="12 and younger")] -> node::state(
        title = "prices<12",
        message = "Childer under 12 pay $100 per month",
        prompts = ["more prices", "quit"]
    );

    # this create an edge from prices_12 back to prices.
     prices_12 -[transition(intent="more prices")] -> prices;


}

```
`spawn` is used to create to create child nodes, which is used to design flow of the conversational experience.
We are able to create additional edges to connnect nodes which which do not share a parent -child relationship. This is shown in the last line.

```jac
node state {
    has title;
    has message;
    has prompts;
}


edge transition {
    has intent;
}

graph main_graph {
    has anchor main_root;

    spawn {

        main_root = spawn node::state(
        title = "Welcome",
        message = "Welcome to Jaseci Dojo, how can i help?",
        prompts = ["class","times","prices","quit"]
    );

    prices = spawn main_root -[transition(intent="prices")] -> node::state(
        title = "prices",
        message = "Prices Vary based on age",
        prompts = ["12 and younger", "18 and younger" ,"Older than 18", "quit"]
    );

    prices_12 = spawn prices -[transition(intent="12 and younger")] -> node::state(
        title = "prices<12",
        message = "Childer under 12 pay $100 per month",
        prompts = ["more prices", "quit"]
    );
     prices_12 -[transition(intent="more prices")] -> prices;

     prices_18 = spawn prices -[transition(intent="18 and younger")] -> node::state(
        title = "prices<18",
        message = "Childer under 18 pay $110 per month",
        prompts = ["more prices", "quit"]
    );

    prices_18 -[transition(intent="more prices")] -> prices;

     pricesabove18 = spawn prices -[transition(intent="Older than 18")] -> node::state(
        title = "pricesadults",
        message = "Adults over 18 pay $150 per month",
        prompts = ["more prices","quit"]
    );
     pricesabove18 -[transition(intent="more prices")] -> prices;


    class = spawn main_root -[transition(intent="class")]-> node::state(
        title = "class",
        message = "There are 3 classes per week and you are required to attend a minimum of 2.",
        prompts = ["time","days","prices","quit"]

    );



    time = spawn class -[transition(intent="time")]-> node::state(
        title = "time",
        message = "Classes are from 3 pm to 4 pm",
        prompts = ["other times","days","quit"]
    );

    main_root -[transition(intent="times")] -> time;

    other_time = spawn time -[transition(intent="other times")]-> node::state(
        title = "Other times",
        message ="The clases are at 4 pm to 5 pm but you need at least 4 other students to start",
        prompts = ['days',"quit"]
    );




     days = spawn time -[transition(intent="days")]-> node::state(
        title = "days",
        message ="The classes are on Monday ,Wednesday , Friday",
        prompts = ['time',"quit"]
    );


     other_time - [transition(intent="days")] -> days ;
     days - [transition(intent="time")] -> time ;

    }
}

```
This last code block we created several nodes and connected them together. To move from node to node we use the intent to sepcify which route to take.

### Walker
* Walkers traverse the nodes of the graph triggering execution at the node level.

Now lets create a file called walker.jac
Here is where we will create  the method for traveral of the graph.

```jac

#here we initialize the walker which we named talker.
walker talker {

    has utterance;

    state {
        #prints out the message and prompts variables for the node the walker is currently on
        std.out(here.message,here.prompts);

        #here we take the input from the terminal.
        utterance =  std.input("> ");

        #if the user enters "quit" the programs ends.
        if(utterance=="quit"): disengage;

        #checks the utterance and determine which node to traverse too.
        take -[transition(intent==utterance )] -> node::state else{
            take here ;
        }
    }

}

```

The Walker will start from the main root and from the utterance intered it will determine which node to go to next.
It should be noted the utterance must match the prompts chosen or the walker will not move from the graph.
Jaseci-ai-kit has features that makes it possible for users to not enter the exact intent but still traverse to the right node.

### Main

Create a file named main.jac .

```jac
# import the graph and walker made earlier.
import {*} with "./graph.jac";
import {*} with "./walker.jac";

# this walker is reponsible for starting the program.
walker init {

    root {
        #creates an instant of the graph
        spawn here --> graph::main_graph;

        #creates an instance of the walker, talker
        spawn  --> walker::talker;
    }


}

```

Once we run main.jac we can use the Chatbot. Play around with graph and add your own nodes and link other nodes together to create an even better chatbot.
