---
sidebar_position: 1
---

# Quick Start

Hi! The First thought comes to our mind after knowing that we have to learn a new programming language, Jaseci is, WHY, a new language?
Let's achieve the answer together.

# Jaseci is a computational model and a language in one unit
In simple words, **Jaseci** provides a platform where you can implement the **SOTA** AI modules without taking the pain of training or hosting them.


## Starting With Jaseci
1. Getting **Jac** in your local system:
   1. Pypi Installation : pip install jaseci-core (gets you the latest jac version)
   2. getting from the github :
      1.  git clone https://github.com/Jaseci-Labs/jaseci.git
      2.  cd  **jaseci_core**
      3.   bash install.sh
2. Starting With **jsctl** :
   1. once you execute  **jsctl** command in terminal, jaseci command line shell it activated.

            jsctl
            Starting Jaseci Shell...
            jaseci >
   2.  type `help`

            jaseci > help

            Documented commands (type help <topic>):
            ========================================
            actions    clear   global  logger  master  sentinel  walker
            alias      config  graph   login   object  stripe
            architype  edit    jac     ls      reset   tool

            Undocumented commands:
            ======================
            exit  help  quit

    3. You'll get all available commands  in **Jaseci**. For getting details on command you can type :

            jaseci > graph --help
            Usage: graph [OPTIONS] COMMAND [ARGS]...

            Group of `graph` commands

            Options:
            --help  Show this message and exit.

            Commands:
            active  Group of `graph active` commands
            create  Create a graph instance and return root node graph object
            delete  Permanently delete graph with given id
            get     Return the content of the graph with mode Valid modes: {default,...
            list    Provide complete list of all graph objects (list of root node...
            node    Group of `graph node` commands
## Coding the Jac File
1. Before jumping into the code let's know about the building blocks of jac programming. Everything in **Jac** is about graph, therefore, **Nodes** and **Edges** are the main constituient of jac programming, now to traverse through graph **Jac** has a superman known as **Walker**.

2. **Hello World** :
Let's Start with our first Jac program.

```jac
walker init {
    std.out("hello world");
}
```

Save the above code in `hello_world.jac` file in the current working directory.

To run the jac code you simple have to :

    jaseci > jac run hello_world.jac
    2022-03-14 16:24:35,847 - INFO - parse_jac: default: Processing Jac code...
    2022-03-14 16:24:35,905 - INFO - register: default: Successfully registered code
    hello world
Let's get into the details, `walker` is keyword used to define a **Walker**, `init` is a reserved word which in this case provides the entry point to the jac program. Therefore, once the compiler encounter `walker init {}` it start the execution, line 2 contains, `std` library for standard operation and `out()` is a module for printing, so the command `std.out()`  helps in displaying the passed text `Hello World` on the command prompt.

3. Let's consised a full jac program. The program is to create a family having a man , a womam, a son and show the relations between them:

```jac
node person;
node man;
node woman;

edge mom;
edge dad;
edge married;

walker init {
root {
    spawn here --> node::man;
    spawn here --> node::woman;
    --> node::man <-[married]-> --> node::woman;
    take -->;
    }
    woman {
    son = spawn here <-[mom]- node::person;
    son -[dad]-> <-[married]->;
    }
    man {
        std.out("I␣didnt␣do␣any␣of␣the␣hard␣work.");
    }
}
```

Executing the above code:
```
jaseci > graph create
{
"context": {},
"anchor": null,
"name": "root",
"kind": "generic",
"jid": "urn:uuid:7b218b7a-ba38-4fbd-a5c8-ef8bdc33dfff",
"j_timestamp": "2022-03-14T14:31:30.823169",
"j_type": "graph"
}
jaseci > sentinel register -name family -code fam.jac
2022-03-14 20:01:53,768 - INFO - parse_jac: family: Processing Jac code...
2022-03-14 20:01:53,797 - INFO - register: family: Successfully registered code
I didnt do any of the hard work.
```

So, we create a root graph by executing `graph create`, then we register our code with a sentinel using the command `sentinel register -name family -code fam.jac` where **family** is the nae of the sentinel and **fam.jac** is the file containing the jac code to be register.

Lets get into details of the code:

```jac
// Declaring the nodes required for the program -
node person;
​node man;
​node woman;

Edges required for depicting the relations -
edge mom;
edge dad;
edge married;

walker init { //declaring the walker

    // the root block contains the code related to root node
    root { // declaring root block
        spawn here --> node::man; // spawn a reserverd keyword to spwan or instantiate anything, a new node of type man, in this case.
        spawn here --> node::woman; // spwaning a node of type `woman` from root `node`
        --> node::man <-[married]-> --> node::woman; // this line does 2 operations, firstly, take the edge from root node to node man, then create a bi-directional edge of type married from mam to woman
        take -->; // this line instructs to take the edge available, i.e. from man to woman
    }

    // the woman block contains connection code with child
    woman {
        son = spawn here <-[mom]- node::person; // creates node of type person from current location i.e. from woman node and assign it to son
        son -[dad]-> <-[married]->;  // this line can also be written as :- son -[dad]-> node::man; , which mean create a edge from son to man.
    }
    // the man block didn't have any task, so we just did a std.out()
    man {
        std.out("I␣didnt␣do␣any␣of␣the␣hard␣work.");
    }
```

The below graph can help us understand the jac code.

![Graph Family](/img/tutorial/getting_started/fam.jpg)

 4. Hopefully we're starting to understand the nuances of jac. To get a better understanding let's take another example.
### code:

```jac
node person{
    has name;
    has byear;
    can set_year with setter entry{
        byear = visitor.year;
    }
    can print_out with exit{
        std.out(byear," from ", visitor.info);
    }
    can reset{
        ::set_back;
        std.out("resetting birth year to 2000 : ", here.context);
    }
    can set_back : byear = "2000-01-01";
}

walker init {
    has year=std.time_now();
    can setup{
        person1 = spawn here --> node::person(name="Ashish");
        std.out("node id : ",person1);
        person1::reset;
    }
    root{
        ::setup;
        take --> ;
    }
    person{
        spawn here walker::setter;
        here::reset(name="Joe");
    }
}

walker setter{
    has year="2008-11-19";
}
```

### output:

```
node id :  jac:uuid:fee335b6-db23-49c4-84c9-8161c4d0c055
resetting birth year to 2000 :  {}
2008-11-19  from  {"context": {"year": "2008-11-19"}, "anchor": null, "name": "setter", "kind": "walker", "jid": "urn:uuid:336e56cd-4440-4835-9ae8-1484e78b2556", "j_timestamp": "2022-03-15T12:39:27.398912", "j_type": "walker"}
resetting birth year to 2000 :  {"name": "Joe", "byear": "2000-01-01"}
2000-01-01  from  {"context": {"year": "2022-03-15T12:39:27.391920"}, "anchor": null, "name": "init", "kind": "walker", "jid": "urn:uuid:71055778-86cd-47b7-8410-6c6039fe3318", "j_timestamp": "2022-03-15T12:39:27.391920", "j_type": "walker"}
```

Lets get into details of the code :

```jac
// One of the important features of jac is even nodes and edges cam store information, below we have a node that has atrributes and blocks with entry, exit and activity criteria
node person{ // declaring a node block person
    has name; // node person has a name
    has byear; // it also has birthyear as byear
    can set_year with setter entry{ // node block has a can block that will only be

    executed with setter entry
        byear = visitor.year; //visitor is the object's active instance, wecan access
        // the properties of object by calling "visitor.<property>"
    }

    can print_out with exit{ //person node has another can block that will be executed with exit of the object instance

        std.out(byear," from ", visitor.info); //visitor.info provides the entiire details about the object call
    }
    can reset{ // a rest block to test the activity other than setter
        ::set_back;  // this statement is used to call the setback block
        std.out("resetting birth year to 2000 : ", here.context); // here is another built-in property that can be used to access the data  of the current instance
    }
    can set_back : byear = "2000-01-01"; // if a block is a one-liner, it can also be declared with " : ", as declared in current line
}

walker init { //declaring the init walker start the execution, in jac walker can also have properties
    has year=std.time_now(); // declaring year as a property
    can setup{ // has a setup block
        person1 = spawn here --> node::person(name="Ashish"); //spwaning a new node
        std.out("node id : ",person1); // prinit the variable gives us the node id
        person1::reset; // call the reset block for current node
    }
    root{ //the root block i excuted initially
        ::setup; // call the setup block
        take --> ; // take the availalbe edge
    }
    person{ // the person block is executed next
        spawn here walker::setter; // we're spawnning the setter walker on person1 node
        here::reset(name="Joe");// from current position reset the name to Joe
    }
}

walker setter{ // the setter walker which has a attribute which is used to set for a particular node
    has year="2008-11-19";
}
```

From the above example we're able to understand how data and functions can be made available in node and walker, how we can use them.

# Appendix
## Interface Parameters
- config delete (name: str, do check: bool = True)
- config exists (name: str)
- config get (name: str, do check: bool = True)
- config list ()
- config set (name: str, value: str, do check: bool = True)
- global delete (name: str)
- global sentinel set (snt: jaseci.actor.sentinel.sentinel = None)
- global sentinel unset ()
- global set (name: str, value: str)
- global get (name: str)
- logger http clear (log: str = ’all’)
- logger http connect (host: str, port: int, url: str, log: str = ’all’)
- logger list ()
- master create super (name: str, set active: bool = True, other fields: dict = )
- master active get (detailed: bool = False)
- master active set (name: str)
- master active unset ()
- master create (name: str, set active: bool = True, other fields: dict = )
- master delete (name: str)
- master get (name: str, mode: str = ’default’, detailed: bool = False)
- master list (detailed: bool = False)
- alias clear ()
- alias delete (name: str)
- alias list ()
- alias register (name: str, value: str)
- architype delete (arch: jaseci.actor.architype.architype, snt: jaseci.actor.sentinel.sentinel = None)
- architype get (arch: jaseci.actor.architype.architype, mode: str = ’default’, detailed: bool = False)
- architype list (snt: jaseci.actor.sentinel.sentinel = None, detailed: bool = False)
- architype register (code: str, encoded: bool = False, snt: jaseci.actor.sentinel.sentinel = None)
- architype set (arch: jaseci.actor.architype.architype, code: str, mode: str = ’default’)
- graph active get (detailed: bool = False)
- graph active set (gph: jaseci.graph.graph.graph)
- graph active unset ()
- graph create (set active: bool = True)
- graph delete (gph: jaseci.graph.graph.graph)
- graph get (gph: jaseci.graph.graph.graph = None, mode: str = ’default’, detailed: bool = False)
- graph list (detailed: bool = False)
- graph node get (nd: jaseci.graph.node.node, ctx: list = None)
- graph node set (nd: jaseci.graph.node.node, ctx: dict, snt: jaseci.actor.sentinel.sentinel = None)
- object get (obj: jaseci.element.element.element, depth: int = 0, detailed: bool = False)
- object perms get (obj: jaseci.element.element.element)
- object perms grant (obj: jaseci.element.element.element, mast: jaseci.element.element.element, read only: bool = False)
- object perms revoke (obj: jaseci.element.element.element, mast: jaseci.element.element.element)
- object perms set (obj: jaseci.element.element.element, mode: str)
- sentinel active get (detailed: bool = False)
- sentinel active global (detailed: bool = False)
- sentinel active set (snt: jaseci.actor.sentinel.sentinel)
- sentinel active unset ()
- sentinel delete (snt: jaseci.actor.sentinel.sentinel)
- sentinel get (snt: jaseci.actor.sentinel.sentinel = None, mode: str = ’default’, detailed: bool = False)
- sentinel list (detailed: bool = False)
- sentinel pull (set active: bool = True, on demand: bool = True)
- sentinel register (name: str, code: str = ”, encoded: bool = False, auto run: str = ’init’, ctx: dict = , set active: bool = True)
- sentinel set (code: str, encoded: bool = False, snt: jaseci.actor.sentinel.sentinel = None, mode: str = ’default’)
- walker delete (wlk: jaseci.actor.walker.walker, snt: jaseci.actor.sentinel.sentinel = None)
- walker execute (wlk: jaseci.actor.walker.walker)
- walker get (wlk: jaseci.actor.walker.walker, mode: str = ’default’, detailed: bool = False)
- walker list (snt: jaseci.actor.sentinel.sentinel = None, detailed: bool = False)
- walker prime (wlk: jaseci.actor.walker.walker, nd: jaseci.graph.node.node = None, ctx: dict = )
- walker register (snt: jaseci.actor.sentinel.sentinel = None, code: str = ”, encoded: bool = False)
- walker run (name: str, nd: jaseci.graph.node.node = None, ctx: dict = , snt: jaseci.actor.sentinel.sentinel = None)
- walker set (wlk: jaseci.actor.walker.walker, code: str, mode: str = ’default’)
- walker spawn (name: str, snt: jaseci.actor.sentinel.sentinel = None)
- walker unspawn (wlk: jaseci.actor.walker.walker)
- walker summon (self, key: str, wlk: jaseci.actor.walker.walker, nd: jaseci.graph.node.node, ctx: dict = )

## Lexer Rules

- TYP_STRING: 'str';
- TYP_INT : 'int';
- TYP_FLOAT : 'float';
- TYP_LIST: 'list ';
- TYP_DICT: 'dict ';
- TYP_BOOL: 'bool';
- KW_TYPE: 'type ';
- KW_GRAPH : 'graph ';
- KW_STRICT: 'strict ';
- KW_DIGRAPH : 'digraph ';
- KW_SUBGRAPH: 'subgraph ';
- KW_NODE : 'node ';
- KW_IGNORE : 'ignore ';
- KW_TAKE : 'take';
- KW_SPAWN: 'spawn';
- KW_WITH: 'with ';
- KW_ENTRY: 'entry';
- KW_EXIT: 'exit' ;
- KW_LENGTH: 'length ';
- KW_KEYS: 'keys ';
- KW_CONTEXT : 'context ';
- KW_INFO: 'info';
- KW_DETAILS:	'details';
- KW_ACTIVITY :  'activity';
- COLON : ' : ' ;
- DBL_ COLON : ' :: ' ;
- COLON_OUT:	'::>';
- LBRACE : '{';
- RBRACE : '}' ;
- KW_EDGE : 'edge ';
- KW_WALKER:	'walker';
- SEMI :  ' ; ' ;
- EQ : '= ' ;
- PEQ : '+= ' ;
- MEQ : '-=' ;
- TEQ : '*= ' ;
- DEQ : '/= ' ;
- CPY_EQ : ' := ' ;
- KW_AND : 'and ' I '&& ' ;
- KW_OR:	'or' I  ' I I ' ;
- KW_ IF:	' if ' ;
- KW_ELIF: 'elif ' ;
- KW_ELSE : 'else';
- KW_FOR : 'for';
- KW_TO : 'to';
- KW_BY : 'by ' ;
- KW_WHILE :  'while ';
- KW_CONTINUE:	'continue ';
- KW_BREAK: 'break ';
- KW_DISENGAGE: 'disengage';
- KW_SKIP: 'skip' ;
- KW_REPORT: 'report';
- KW_DESTROY : 'destroy ';
- DOT: '.';
- NOT: '!' I	'not' ;
- EE: '== ' ;
- LT : '< ' ;
- GT: '> ' ;
- LTE : '<= ' ;
- GTE: '>= ' ;
- NE:	' !-' ;
- KW_IN : 'in';
- KW_ANCHOR : 'anchor';
- KW_HAS : 'has';
- KW_PRIVATE: 'private ';
- COMMA: ',';
- KW_CAN: 'can ';
- PLUS: '+' ;
- MINUS: '-';
- MUL : '*' ;
- DIV: ' I ' ;
- MOD: '%' ;
- POW: '^'
- NULL: 'null'
