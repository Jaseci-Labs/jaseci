# jaseci

## Concepts

### Action

- Actions are computational processing elements. [0]
- Actions take in a list of context items as input and outputs one or many context items. [0]
- All possible actions are provided by Jaseci. [0]
- Actions attached to nodes, edges, etc will search walker, itself, then higher dimentional nodes for input contexts in that order,

### Context

- Context is a list of one or more key-value pairs. [1]

### Nodes and HD Graph Domains and Planes

- Nodes are composed of context and executable actions. [1]
- Nodes accumulate context via a push function, context can be read as well. [1]
- Nodes execute a set of actions upon: [1]
  1. Entry [1]
  2. Exit [1]
- Activity actions in a node denote actions that a walker can call at any time
- Nodes must be aware of the set of HDGDs of which it is a member. [1]
- Nodes must trigger processing of HDGDs of which it is a member upon events. [0]
  - Seperate actions at the HDGDs above can occur on entry and exit events [0]
- At the first dimension, these are essentially subsets of nodes for which there are common traits. Traits can include context both static and dynamic (built over time) or actions to be executed upon []
  1. entry from some edge into the domain from another domain at the given dimensionality,
  2. edge traversals within a domain, or
  3. exits out of the domain to antoher domain at the domains given dimensionality.
- At higher dimensions, these HDGDs are comprised of HDGDs of the next dimension down and function similarly with the element case but instead of nodes they comprise of HDGDs. (HDGD_2 is a graph comprised of HDGD_1 graphs)
- Transitions at a given dimension can only occur between domains of that dimension or to non-domain nodes.
- HDGDs can overlap at a given dimension.
- Each domain at any dimensionality has a root node.
- Transitions at the node level trigger computation in parallel at all dimensions of HDGDs for which that node is a member of.
- Optional:
  - Upon creation of an edge between nodes that is first to span HDGD bounderies at any dimensionality, an edge is created implicity betwen HDGDs at that dimensionality (these edges function exactly like edges between nodes). At this point the edges can carry context and actions.
  - Upon deletion of an edge between nodes that is the last to span HDGD bounderies at any dimensionality, the edge that was created connecting those HDGDs is deleted.
  - Nodes have an anchor context value that is used to represent the 'value' of the node, for example when deciding which outbound node a walker should take based on some evaluation. Each node can select only one element from context to be it's anchor

### Edges

- Edges are composed of context and executable actions [1]
- Edges accumulate context via a push function, context can be read as well [1]
- Edges execute a set of actions when traversed. [0]
- Edges much be aware of the set of HDGDs of which it is a member. [0]
- Edges crossing HDGD boundaries must trigger higher order HDGD plane edges. [0]

### Walkers

- Walkers walk nodes triggering execution at the node level and HDGD levels.
- Walkers can pick up context as they traverse.
- Walkers also decide which node to travel through next and records the path of travel (trail) to be recorded within it's own context.
- Walkers can be spawned at any node.
- Walkers can spawn other walkers.
- Computation happens at the Node and HDGD levels. However walkers make decisions on where to walk next and which context to pick up.
- Walker context must be preloaded by sentinel or applications as a form of input and configuration for the walk
- Walkers can carry with them their own actions and contexts that is executed whenever specified in the walkers own code

### Sentinels

- Sentinels watch walkers, aggregate outcomes of walking, and enact policies.
- Each walker must have a sentinel and the division of labor is
  1. Walkers are concerned primarily for walking the graph.
  2. Sentinels will take the results of one or more walkers to perform some higher order objective (i.e., resolution)
- Keeps context that can be used to save derivitave application behavior.
- Sentials harbor walkers, architype and jac programs that encode walkers and architypes
- Sentials can 'register' Jac programs which is a sort of compile that will generate architypes and walkers
- If the program has syntax errors registration fails, once registered walkers fail at runtime

### Architypes

- Registers templatized version of instances of any Jaseci abstractions or collections of instances (e.g., subgraphs, etc)

### Graph

- A graph is a root node (inhereted from node) and manages sentinels, and higher dimentional nodes

### Masters

- This is the center of management of a jaseci instance that orchestrates the manipulation of graphs

### Jac Language

- Jac is a language for expressing computations using Jaseci concepts.
- Jac is is a means to express the utilization of Jaseci as a machine.
- Walkers can spawn other workers and use the with keyword to specify input context
- Jac encodes the description of architype nodes and edges (with binded contexts and actions)
- Jac describes how walker and sentinel execution should be performed

#### Jac Grammar

    program     : element*

    element     : architype
                : walker

    architype   : KW:NODE (COLON INT)? ID LBRACE attr_stmts RBRACE
                : KW:EDGE ID LBRACE attr_stmts RBRACE

    walker      : KW:WALKER ID code_block

    statements  : statement*

    statement   : architype
                : walker
                : code_block
                : node_code
                : expression SEMI
                : if_stmt
                : for_stmt
                : while_stmt

    code_block  : LBRACE statements RBRACE
                : COLON statement SEMI

    node_code   : dotted_name code_block

    expression  : dotted_name EQ expression
                : compare (KW:AND|KW:OR compare)*

    if_stmt     : KW:IF expr code_block (elif_stmt)* (else_stmt)*

    for_stmt    : KW:FOR expression KW:TO experssion KY:BY expression code_block

    while_stmt  : KW:WHILE expression code_block

    attr_stmts  : attr_stmt*

    dotted_name : ID (DOT ID)*

    compare     : NOT compare
                : arithmetic ((EE|LT|GT|LTE|GTE) arithmetic)*

    attr_stmt   : KW:HAS ID (, ID)* SEMI
                : KW:CAN dotted_name (, dotted_name)* SEMI
                : arch_set SEMI

    arch_set    : KW:NAME EQ expression
                : KW:KIND EQ expression

    arithmetic  : term ((PLUS|MINUS) term)*

    term        : factor ((MUL|DIV) factor)*

    factor      : (PLUS|MINUS) factor
                : power

    power       : func_call (POW factor)*

    func_call   : atom (LPAREN (expression (COMMA expression)*)? RPAREN)?

    atom        : INT|FLOAT|STRING
                : dotted_name (LSQUARE expression RSQUARE)*
                : LPAREN expr RPAREN
                : list

#### Semenatic Notes

- Language essential expresses
  1. the architypes of the graph to be constructed
  2. the walkers of the graph and how they behave on the graph
- Execution means registering these definitions to the machine and execution occurs via api calls to launch walkers
- Initially, reports will come back via API once a walker has completed it's walk, these reports will be a json payload of objects
- When architypes or walkers are defined within walkers/architypes, the internal name inherits outer name in the form a.b.c on the creation of walker c nested in b nested in a
- Cannot make arbitrary assignments to dotted names
- with entry, exit, activity ignored if is has a can statement in walker or edge
- Graphs root nodes hold global context and actions that walkers can access by referring to root as a built in node variable. Scopes inherit actions as part of the live variable call chain

## Notes

- Walkers can encode a language like basic WalkLang
- Each jaseci object in the model is the same with the object instance pickled inside
- Can create a seperate model at the code level for each of the jaseci object types
- Create a separate django app per api with naming jsci\_\*\_api, one per object
- Tables of all jsci objects are kept in mem as part of the user's object and persisted in models
- Create set of loader and saver functions in separate file in element, frist try to load from mem then from DB if needed
- Serializers can live in this file if not in models file
- Nodes need an anchor value for take / takegen type statements in language, take will evaluate expression then travel to connected node with anchor value that matches output
- all reports are concatanated and reported at end of walk
- I need to have context (items) reference owners so i can delete from all owners upon destruction of item

## Important todos

- Allow assignments to array elements
- Add dereferencer to get address of node/edges (get uuid with & instead of .id)
- On JAC compile create /jac/run API for walkers so you can use urls to call walkers

- CONTEXTS ARE DICTS (not elements)
- NODES REPORT OUTBOUDN AND INBOUND AS WELL AS EDGE IDS
- Auto gen get. adn set. for all architypes
- Hack LL Jac code to report what I need in client
- PLAN - In LL check outbound is workette

- Make parent_id in item type an id_list
- Have ID list class auto delete items from store when owner id's go to zero
- ID list class should add and remove owner ids as it is used to record membership of items to other jaseci objects
- If we enforce the rule that all object membership is done through id_lists then this will stay conherent/consistent
- have owner id's keep track of list name it belongs to so the standard mem_hook destroy function can delete from list upon destruction
- Revise teh way walkers and sentinels are saved to persistent store

- Add type check in action protocol for recieving parameters (parameter format check)
- Nix id_list and just do translations of object to ids in the json encoding of antyhign of type element (isinstance(obj, element) added to UUIDEncoder)
- Make json blob auto translate ids even when in variable that is not id_list
- Create separate logger out for stand output from jac library
- Create wrapper for each type in jac and infrastructure for checks on those types and opperations on those types, already done-ish with "jac_set" but needs to apply to lists etc
- If spawns support both jac_sets adn nodes at the moement then we may need infrastructure features around that. Features many need more scalable code architecture
- Need to support here.id root.id my.id etc

### Trickier bugs

- memory db stores, if db is changed then memory become insonsistent, problematic since memory is assumed to be up to date adn write through: jsci_engine_test.py
- Wierd issue where on a load from db, new id is randomly generated in object, then new object is stored back to db: orm_hook.py

## Example Use Cases

### LifeLogify

- Each user has one life node in their model thats a pointer in jaseci node for entire lifelogify account
- Walkers start from this node
- Graph Structure
  1. Each life is a basic HGDG
     1. Children of root are years
     2. Childern of years are months
     3. Childern of months are weeks
     4. Childern of weeks are days
     5. Children of days are workettes
     6. Workettes link back to prior carried over workettes
  2. HDGD maintians last day touched as context
  3. Nodes are only created when days are touched
- Walkers
  1. Walkers used to find days, and load workettes
  2. Walkers used for carry forward functionality

gata put semis in

### Toy script

    node life {
      can infer.year_from_date
    }

    node year {
      has year
      can infer.month_from_date
    }

    node month {
      has month
      can infer.week_from_date
    }

    node week {
      has week
      can infer.day_from_date
    }

    node day {
      has day
    }

    node workette {
      has name
      has date
      has owner
      has status
      has snooze_till
      has note
      has is_MIT
      has is_ritual
    }

    walker get_day {
      has date
      life: take infer.year_from_date(date)
      year: take infer.month_from_date(date)
      month: take infer.week_from_date(date)
      week: take infer.day_from_date(date)
      day: report day.all_outbound
    }

    walker get_gen_day {
      has date
      life: takegen infer.year_from_date(date)
      year: takegen infer.month_from_date(date)
      month: takegen infer.week_from_date(date)
      week: takegen infer.day_from_date(date)
      day: report day.outbound_nodes
    }

    walker get_sub_workettes {
      workette: report day.outbound_nodes
    }

    walker get_latest_day {
      life: take year.max_outbound
      year: take month.max_outbound
      month: take week.max_outbound
      week: report day.max_outbound
    }

    walker carry_forward {
      has my_root
      day {
        spawn node.day new_day
        my_root = new_day
        take day.outbound_nodes
      }
      workette {
        if(workette.status == 'done' or 'eliminated') { continue }
        spawn node.workette new_workette
        new_workette.connectfrom workette
        new_workette.connectfrom my.spawn.node.last(-1)
        takeall workette.outbound_nodes with {
          is not new_workette
          is untraveled
        }
      }
      report spawn.all
      report my_root
    }
