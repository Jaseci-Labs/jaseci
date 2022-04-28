---
sidebar_position: 2
---

# Getting to know Jaseci

## What is Jaseci

**Jaseci** is a computational model and a language in one unit. Read on.

## Why Jaseci?

Over the last decade we came a far way when it comes to building and developing AI models but most of the solutions out there, well, they require lots of work when compared to a system like Jaseci, which brings to the table an all in one solution to building simple to complex AI models.

Lets' imagine a developer wants to build an AI model to classify and group similar photos of Animals or Cars. The developer would begin by researching what AI models to use to accomplish the work he is trying to do. Once we finalizes on a model from hundreds of models existing models he would have to integrate the model into python then build out APIs for training and testing. What we've just mentioned would take days, maybe even weeks if you haven't got a good grip of knowledge of AI models... Because of this long pain staking process we were motivated to build Jaseci.

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
