# Welcome to the Jaseci Tutorial

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
   1. once you fire **jsctl** command in out terminal, jaseci command line shell it activated.
        
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
            
    1. You'll get all available commands  in **Jaseci**
    2. For getting details on command you can type :
         
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

        walker init {
        std.out("hello world");
        }
    Save the above code in `hello_world.jac` file in the current working directory.

    To run the jac code you simple have to :

        jaseci > jac run hello_world.jac
        2022-03-14 16:24:35,847 - INFO - parse_jac: default: Processing Jac code...
        2022-03-14 16:24:35,905 - INFO - register: default: Successfully registered code
        hello world
    Let's get into the details, `walker` is keyword used to define a **Walker**, `init` is a reserved word which in this case provides the entry point to the jac program. Therefore, once the compiler encounter `walker init {}` it start the execution, line 2 contains, `std` library for standard operation and `out()` is a module for printing, so the command `std.out()`  helps in displaying the passed text `Hello World` on the command prompt.

3. Let's consised a full jac program:
   
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
                take -->; }
            woman {
                son = spawn here <-[mom]- node::man;
                son -[dad]-> <-[married]->;
            }
            man {
                std.out("I␣didn’t␣do␣any␣of␣the␣hard␣work.");
            }
        }
    Executing the above code : 

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
        [
        {
            "version": null,
            "name": "family",
            "kind": "generic",
            "jid": "urn:uuid:9a59c26f-d518-4b91-89ba-e1a0e53640c3",
            "j_timestamp": "2022-03-14T14:31:53.767279",
            "j_type": "sentinel"
        },
        {
            "context": {},
            "anchor": null,
            "name": "root",
            "kind": "generic",
            "jid": "urn:uuid:d80a52d3-efbb-4c50-96e5-2a99507dfac9",
            "j_timestamp": "2022-03-14T14:31:53.768278",
            "j_type": "graph"
        }
        ]
    So, we create a root graph by executing `graph create`, then we register our code with a sentinel using the command `sentinel register -name family -code fam.jac` where **family** is the nae of the sentinel and **fam.jac** is the file containing the jac code to be register.

    The below graph can help us understand the jac code.

    ![Graph Family](fam.jpg)

    



# Appendix 
## Interface Parameters
    config delete (name: str, do check: bool = True)
    config exists (name: str)
    config get (name: str, do check: bool = True)
    config list ()
    config set (name: str, value: str, do check: bool = True)
    global delete (name: str)
    global sentinel set (snt: jaseci.actor.sentinel.sentinel = None)
    global sentinel unset ()
    global set (name: str, value: str)
    global get (name: str)
    logger http clear (log: str = ’all’)
    logger http connect (host: str, port: int, url: str, log: str = ’all’)
    logger list ()
    master createsuper (name: str, set active: bool = True, other fields: dict = )
    master active get (detailed: bool = False)
    master active set (name: str)
    master active unset ()
    master create (name: str, set active: bool = True, other fields: dict = )
    master delete (name: str)
    master get (name: str, mode: str = ’default’, detailed: bool = False)
    master list (detailed: bool = False)
    alias clear ()
    alias delete (name: str)
    alias list ()
    alias register (name: str, value: str)
    architype delete (arch: jaseci.actor.architype.architype, snt:
    jaseci.actor.sentinel.sentinel = None)
    architype get (arch: jaseci.actor.architype.architype, mode: str = ’default’, detailed: bool = False)
    architype list (snt: jaseci.actor.sentinel.sentinel = None, detailed: bool = False)
    architype register (code: str, encoded: bool = False, snt:
    jaseci.actor.sentinel.sentinel = None)
    architype set (arch: jaseci.actor.architype.architype, code: str, mode: str =
    ’default’)
    graph active get (detailed: bool = False)
    graph active set (gph: jaseci.graph.graph.graph)
    graph active unset ()
    graph create (set active: bool = True)
    graph delete (gph: jaseci.graph.graph.graph)
    graph get (gph: jaseci.graph.graph.graph = None, mode: str = ’default’,
    detailed: bool = False)
    graph list (detailed: bool = False)
    graph node get (nd: jaseci.graph.node.node, ctx: list = None)
    graph node set (nd: jaseci.graph.node.node, ctx: dict, snt:
    jaseci.actor.sentinel.sentinel = None)
    object get (obj: jaseci.element.element.element, depth: int = 0, detailed:
    bool = False)
    object perms get (obj: jaseci.element.element.element)
    object perms grant (obj: jaseci.element.element.element, mast:
    jaseci.element.element.element, read only: bool = False)
    object perms revoke (obj: jaseci.element.element.element, mast:
    jaseci.element.element.element)
    object perms set (obj: jaseci.element.element.element, mode: str)
    sentinel active get (detailed: bool = False)
    sentinel active global (detailed: bool = False)
    sentinel active set (snt: jaseci.actor.sentinel.sentinel)
    sentinel active unset ()
    sentinel delete (snt: jaseci.actor.sentinel.sentinel)
    sentinel get (snt: jaseci.actor.sentinel.sentinel = None, mode: str = ’default’,
    detailed: bool = False)
    sentinel list (detailed: bool = False)
    sentinel pull (set active: bool = True, on demand: bool = True)
    sentinel register (name: str, code: str = ”, encoded: bool = False, auto run: str
    = ’init’, ctx: dict = , set active: bool = True)
    sentinel set (code: str, encoded: bool = False, snt:
    jaseci.actor.sentinel.sentinel = None, mode: str = ’default’)
    walker delete (wlk: jaseci.actor.walker.walker, snt: jaseci.actor.sentinel.sentinel
    = None)
    walker execute (wlk: jaseci.actor.walker.walker)
    walker get (wlk: jaseci.actor.walker.walker, mode: str = ’default’, detailed:
    bool = False)
    walker list (snt: jaseci.actor.sentinel.sentinel = None, detailed: bool = False)
    walker prime (wlk: jaseci.actor.walker.walker, nd: jaseci.graph.node.node =
    None, ctx: dict = )
    walker register (snt: jaseci.actor.sentinel.sentinel = None, code: str = ”, encoded:
    bool = False)
    walker run (name: str, nd: jaseci.graph.node.node = None, ctx: dict = , snt:
    jaseci.actor.sentinel.sentinel = None)
    walker set (wlk: jaseci.actor.walker.walker, code: str, mode: str = ’default’)
    walker spawn (name: str, snt: jaseci.actor.sentinel.sentinel = None)
    walker unspawn (wlk: jaseci.actor.walker.walker)
    walker summon (self, key: str, wlk: jaseci.actor.walker.walker, nd:
    jaseci.graph.node.node, ctx: dict = )

