---
sidebar_position: 1
---

# Getting to know Jaseci

## What is Jaseci

**Jaseci** is an end-to-end open-source and Open Computational Model, Technology Stack, and Methodology for bleeding edge AI. It enables developers to rapidly build robust products with sophisticated AI capabilities at scale.

## Why Jaseci?

- Jaseci has powerful AI models which any developer can leverage in their application quickly and easily.
- Jaseci Diffuse Runtime System , this runtime system handles the orchestration , configuration and optimization of the full cloud compute stack and inter-machine resources such as container formation , scaling and optimization . In essence it provides all the technology needed to develop an AI application in one platform.
- Reduce Development team specializations. You'll only need a single Jaseci Engineer to do the work of DevOps Engineers, Frontend and Backend engineers and AI engineers.
- Solve problems more readily with a graph-based representation of data.
- Accelerate the development time of any AI application.
- Save time with automatically generated APIs.

## How Jaseci works 
Jaseci brings application development, AI Models and code infrastructure together under a single solution stack. Using the JAC Programming language you are able to leverage all the goodness that Jaseci has to offer such as wielding powerful AI models and exposing complex business logic via automatically generated APIs . 
Jaseci can either be used to build a centralized or distributed system. It depends how the developer creates their sentinel. You can think of a sentinel in Jaseci as a representation of a JAC program. Each sentinel has its own ID and contains within it, all addressable walkers and operations which may be called via the API.  The JAC program that the sentinel represents, is designed to interact with graph data. Typically, each user account in Jaseci owns its own graph data with private permissions to read and write to this user graph data. In addition, each user account has its own sentinel. Usually, this user-based sentinel of non superuser accounts, specifies an active sentinel reference that points to the sentinel of the superuser. This allows the superuser's sentinel code to execute on the respective graph data of each user account. This can, however, be modified which permits each user account to run its own sentinel code. Further, each sentinel refers to an active graph upon which the sentinel code may execute; this typically points to the respective user graphs but may be configured to refer to a centralized graph belonging to the super user, depending on your choice of architecture. With each user account in Jaseci possessing the ability to have its own sentinel and graph, it opens up tons of possibilities for great flexibility (and security) and allows backend code and data to be specific to each user.



![Diagram of superuser](/img/tutorial/getting_started/Superuser.jpeg)

### Centralized System. 

When you create any JAC program you can easily expose your Program to API calls.The Centralized system has a main Sentinel . This main sentinel is set to be globall accessible and active . This is the Sentinel users will connect to , to interact and make changes to their graph.

![Diagram of centeralized system](/img/tutorial/centralized.jpeg)


### Distributed System 
Each person can have their own sentinel. Users can create their Sentiensl based on JAC code they have written. This Sentinel can be made live and is capable of interacting with the users's graph data. This allows for much flexibility with each users own backend code.
[inserts pics o distributed system]

![Diagram of Distributed system](/img/tutorial/Distributed.jpeg)


## Solutions Jaseci provides

Developing AI models with Jaseci is way faster. Its requires 60% less effort when building with Jaseci. Here's why:

- Jaseci is a self-contained system
- Provides API endpoints out of the box to accompany the model you are developing
- Removes data management from your workflow
- Includes scalable deployment with Kubernetes
- Jaseci is a well structured stack
- Jaseci comes with pre-built, pre-trained AI models for most AI Related tasks out of the box.
- You only focus focus on building your solution instead of reinventing the wheel

## Computation and Language

As mentioned above the computation model and language is what makes up the Jaseci Engine. We develop an easy programming language called Jac to manage what you build with Jaseci in a simple way. The language used for interacting with the Jaseci Engine and it gives us the developers control over Jaseci when building AI applications. Using the Jac language, we can leverage the true power of Jaseci.

## Data in Jaseci

### How data is represented

In this section we'll discuss what graphs are. The following video [Basic Graph Theory I - vertices, edges, loops, and equivalent graphs](https://www.youtube.com/watch?v=2RdnHdbgvNg) does a good job of explaining the fundamentals of graph theory, but if you prefer to read on before watching the video we have simplified some fundamental concepts of graph theory in the below sections.


### Understanding Graphs

To help you understand graphs lets consider a section the following diagram that represents a road map.

![Diagram of a road map](/img/tutorial/getting_started/introduction_to_graphs_road_map.png)

Its important to note that the intersection of the line PS and QT is not a vertex.

The points P, Q, R, S and T are called vertices, the lines are called edges, and the whole diagram is called a graph.

This is all you need know about about graphs in order to learn Jaseci. If you would like to know more about graphs outside the scope of what we have just discussed, there are plenty of valuable books and other resources about graph theory.

### Graphs in Jaseci

Jaseci builds an abstraction layer on top of graphs to carryout tasks and instruction written by a developer in Its .jac File (More on this later).

Remember Vertices and Edges?

In Jaseci, we refer to as vertex as a node (Where two points meet) and you can imagine P, Q, R and S as simply nodes.

### Nodes in Jaseci

Nodes in Jaseci can be seen as autonomous. It can carryout its own tasks independently, store data, retrieve data etc. without depending on other nodes.

### Edges in Jaseci

Edges are the links that connect nodes to each other

### What Else? (Walkers)

We talked about Nodes, and Edges but how does it all function. Lets introduce Walkers

Walkers in Jaseci can be imagined as dumb robots that uses the edges of the graph to move from node to node while performing some predefined action. and we get the define the actions walkers should perform in a .jac file.
