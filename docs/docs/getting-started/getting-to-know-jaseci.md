---
sidebar_position: 1
---

# Getting to know Jaseci

## What is Jaseci

**Jaseci** is an end-to-end open-source and Open Computational Model, Technology Stack, and Methodology for bleeding edge AI. It enables developers to rapidly build robust products with sophisticated AI capabilities at scale.

## Why Jaseci?

- Jaseci has powerful AI models which any developer can leverage in their application quickly and easily.
- Jaseci Diffuse Runtime System , this runtime system handles the orchestraation , configuration and optimization of the full cloud compute stack and inter-machine resources such as container formation , scaling and optimization . In essence it provids all the technoloy needed to develop an AI application in one platform.
- Reduce Development teams which comprises of Devops Engineer , Front and Backend Engineer , AI engineers to a single Jaseci Engineer.
- Solve problems with graph representation of data.
- Accelearate Development time of any AI application.
- APIs are automatically genearted .

## How Jaseci works 

Jaseci brings together the Application Developement , AI Models and Code Infrastructure together in to one solution. Using the JAc Programming language you are able to load  AI models and create APIs . 
Jaseci can be either a centralized or Distributed system. It depends how the developer creates their sentinel. What is a sentinel ? A sentinel is the logic that interacts and changes Graph data. All  users of your program will have their own sentinel , this allows for much flexibilty for backend code as it can be specific to each user. Each user also have their own Graph . In reality their 'own graph'  is just their information virtually segmented from the main graph.

[insert pic of super user sentinel]

### Centralized System. 

When you create any JAC program you can easily expose your Program to API calls.The Centralized system has a main Sentinel . This main sentinel is set to be globall accessible and active . This is the Sentinel users will connect to , to interact and make changes to their graph.

[inserts pics of centralized design]

### Distributed System 
Each person can have their own sentinel. Users can create their Sentiensl based on JAC code they have written. This Sentinel can be made live and is capable of interacting with the users's graph data. This allows for much flexibility with each users own backend code.
[inserts pics o distributed system]




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
