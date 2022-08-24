# An Overview of the JAC Language

JAC is the official programming language of Jaseci, specifically designed for developers to author the computational logic which governs the various Jaseci constructs such as libraries, walkers, nodes, edges and graphs. Syntactically, JAC draws from JavaScript and Python but it brings a variety of graph-based operators and expressions that go with the unique development paradigm of Jaseci.

To get acquainted with JAC, you'll first have to understand its various constructs which are governed by the language. Here's an overview of the Jaseci constructs and related terms:

### Action

- Actions are computational processing elements. 
- Actions take in a list of context items as input and outputs one or many context items. 
- All possible actions are provided by Jaseci. 
- Actions attached to nodes, edges, etc will search walker, itself, then higher dimentional nodes for input contexts in that order,

### Context

- Context is a list of one or more key-value pairs. 

### Nodes and HD Graph Domains and Planes

- Nodes are composed of context and executable actions. 
- Nodes accumulate context via a push function, context can be read as well. 
- Nodes execute a set of actions upon: 
  1. Entry 
  2. Exit 
- Activity actions in a node denote actions that a walker can call at any time
- Nodes must be aware of the set of HDGDs of which it is a member. 
- Nodes must trigger processing of HDGDs of which it is a member upon events. 
  - Seperate actions at the HDGDs above can occur on entry and exit events 
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

- Edges are composed of context and executable actions 
- Edges accumulate context via a push function, context can be read as well 
- Edges execute a set of actions when traversed. 
- Edges much be aware of the set of HDGDs of which it is a member. 
- Edges crossing HDGD boundaries must trigger higher order HDGD plane edges. 

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

- This is the center of management of a jaseci instance that orchestrates the manipulation of graphs# An Overview of the JAC Language

JAC is the official programming language of Jaseci, specifically designed for developers to author the computational logic which governs the various Jaseci constructs such as libraries, walkers, nodes, edges and graphs. Syntactically, JAC draws from JavaScript and Python but it brings a variety of graph-based operators and expressions that go with the unique development paradigm of Jaseci.

To get acquainted with JAC, you'll first have to understand its various constructs which are governed by the language. Here's an overview of the Jaseci constructs and related terms:

### Action

- Actions are computational processing elements. 
- Actions take in a list of context items as input and outputs one or many context items. 
- All possible actions are provided by Jaseci. 
- Actions attached to nodes, edges, etc will search walker, itself, then higher dimentional nodes for input contexts in that order,

### Context

- Context is a list of one or more key-value pairs. 

### Nodes and HD Graph Domains and Planes

- Nodes are composed of context and executable actions. 
- Nodes accumulate context via a push function, context can be read as well. 
- Nodes execute a set of actions upon: 
  1. Entry 
  2. Exit 
- Activity actions in a node denote actions that a walker can call at any time
- Nodes must be aware of the set of HDGDs of which it is a member. 
- Nodes must trigger processing of HDGDs of which it is a member upon events. 
  - Seperate actions at the HDGDs above can occur on entry and exit events 
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

- Edges are composed of context and executable actions 
- Edges accumulate context via a push function, context can be read as well 
- Edges execute a set of actions when traversed. 
- Edges much be aware of the set of HDGDs of which it is a member. 
- Edges crossing HDGD boundaries must trigger higher order HDGD plane edges. 

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

- This is the center of management of a jaseci instance that orchestrates the manipulation of graphs# An Overview of the JAC Language

JAC is the official programming language of Jaseci, specifically designed for developers to author the computational logic which governs the various Jaseci constructs such as libraries, walkers, nodes, edges and graphs. Syntactically, JAC draws from JavaScript and Python but it brings a variety of graph-based operators and expressions that go with the unique development paradigm of Jaseci.

To get acquainted with JAC, you'll first have to understand its various constructs which are governed by the language. Here's an overview of the Jaseci constructs and related terms:

### Action

- Actions are computational processing elements. 
- Actions take in a list of context items as input and outputs one or many context items. 
- All possible actions are provided by Jaseci. 
- Actions attached to nodes, edges, etc will search walker, itself, then higher dimentional nodes for input contexts in that order,

### Context

- Context is a list of one or more key-value pairs. 

### Nodes and HD Graph Domains and Planes

- Nodes are composed of context and executable actions. 
- Nodes accumulate context via a push function, context can be read as well. 
- Nodes execute a set of actions upon: 
  1. Entry 
  2. Exit 
- Activity actions in a node denote actions that a walker can call at any time
- Nodes must be aware of the set of HDGDs of which it is a member. 
- Nodes must trigger processing of HDGDs of which it is a member upon events. 
  - Seperate actions at the HDGDs above can occur on entry and exit events 
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

- Edges are composed of context and executable actions 
- Edges accumulate context via a push function, context can be read as well 
- Edges execute a set of actions when traversed. 
- Edges much be aware of the set of HDGDs of which it is a member. 
- Edges crossing HDGD boundaries must trigger higher order HDGD plane edges. 

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

- This is the center of management of a jaseci instance that orchestrates the manipulation of graphs# An Overview of the JAC Language

JAC is the official programming language of Jaseci, specifically designed for developers to author the computational logic which governs the various Jaseci constructs such as libraries, walkers, nodes, edges and graphs. Syntactically, JAC draws from JavaScript and Python but it brings a variety of graph-based operators and expressions that go with the unique development paradigm of Jaseci.

To get acquainted with JAC, you'll first have to understand its various constructs which are governed by the language. Here's an overview of the Jaseci constructs and related terms:

### Action

- Actions are computational processing elements. 
- Actions take in a list of context items as input and outputs one or many context items. 
- All possible actions are provided by Jaseci. 
- Actions attached to nodes, edges, etc will search walker, itself, then higher dimentional nodes for input contexts in that order,

### Context

- Context is a list of one or more key-value pairs. 

### Nodes and HD Graph Domains and Planes

- Nodes are composed of context and executable actions. 
- Nodes accumulate context via a push function, context can be read as well. 
- Nodes execute a set of actions upon: 
  1. Entry 
  2. Exit 
- Activity actions in a node denote actions that a walker can call at any time
- Nodes must be aware of the set of HDGDs of which it is a member. 
- Nodes must trigger processing of HDGDs of which it is a member upon events. 
  - Seperate actions at the HDGDs above can occur on entry and exit events 
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

- Edges are composed of context and executable actions 
- Edges accumulate context via a push function, context can be read as well 
- Edges execute a set of actions when traversed. 
- Edges much be aware of the set of HDGDs of which it is a member. 
- Edges crossing HDGD boundaries must trigger higher order HDGD plane edges. 

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

- This is the center of management of a jaseci instance that orchestrates the manipulation of graphs# An Overview of the JAC Language

JAC is the official programming language of Jaseci, specifically designed for developers to author the computational logic which governs the various Jaseci constructs such as libraries, walkers, nodes, edges and graphs. Syntactically, JAC draws from JavaScript and Python but it brings a variety of graph-based operators and expressions that go with the unique development paradigm of Jaseci.

To get acquainted with JAC, you'll first have to understand its various constructs which are governed by the language. Here's an overview of the Jaseci constructs and related terms:

### Action

- Actions are computational processing elements. 
- Actions take in a list of context items as input and outputs one or many context items. 
- All possible actions are provided by Jaseci. 
- Actions attached to nodes, edges, etc will search walker, itself, then higher dimentional nodes for input contexts in that order,

### Context

- Context is a list of one or more key-value pairs. 

### Nodes and HD Graph Domains and Planes

- Nodes are composed of context and executable actions. 
- Nodes accumulate context via a push function, context can be read as well. 
- Nodes execute a set of actions upon: 
  1. Entry 
  2. Exit 
- Activity actions in a node denote actions that a walker can call at any time
- Nodes must be aware of the set of HDGDs of which it is a member. 
- Nodes must trigger processing of HDGDs of which it is a member upon events. 
  - Seperate actions at the HDGDs above can occur on entry and exit events 
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

- Edges are composed of context and executable actions 
- Edges accumulate context via a push function, context can be read as well 
- Edges execute a set of actions when traversed. 
- Edges much be aware of the set of HDGDs of which it is a member. 
- Edges crossing HDGD boundaries must trigger higher order HDGD plane edges. 

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

- This is the center of management of a jaseci instance that orchestrates the manipulation of graphs# An Overview of the JAC Language

JAC is the official programming language of Jaseci, specifically designed for developers to author the computational logic which governs the various Jaseci constructs such as libraries, walkers, nodes, edges and graphs. Syntactically, JAC draws from JavaScript and Python but it brings a variety of graph-based operators and expressions that go with the unique development paradigm of Jaseci.

To get acquainted with JAC, you'll first have to understand its various constructs which are governed by the language. Here's an overview of the Jaseci constructs and related terms:

### Action

- Actions are computational processing elements. 
- Actions take in a list of context items as input and outputs one or many context items. 
- All possible actions are provided by Jaseci. 
- Actions attached to nodes, edges, etc will search walker, itself, then higher dimentional nodes for input contexts in that order,

### Context

- Context is a list of one or more key-value pairs. 

### Nodes and HD Graph Domains and Planes

- Nodes are composed of context and executable actions. 
- Nodes accumulate context via a push function, context can be read as well. 
- Nodes execute a set of actions upon: 
  1. Entry 
  2. Exit 
- Activity actions in a node denote actions that a walker can call at any time
- Nodes must be aware of the set of HDGDs of which it is a member. 
- Nodes must trigger processing of HDGDs of which it is a member upon events. 
  - Seperate actions at the HDGDs above can occur on entry and exit events 
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

- Edges are composed of context and executable actions 
- Edges accumulate context via a push function, context can be read as well 
- Edges execute a set of actions when traversed. 
- Edges much be aware of the set of HDGDs of which it is a member. 
- Edges crossing HDGD boundaries must trigger higher order HDGD plane edges. 

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