---
sidebar_position: 1
description: Full Specification of Jaseci 2
title: Jaseci 2 Full Spec
---

# Jaseci 2 Design Specifications

## Introduction

Jaseci 2 is the next version of the computational runtime stack, designed to support data-spatial programming and provide a seamless integration with CPython. This document outlines the key features and changes in Jaseci 2, including the retention of novel data-spatial abstractions, full CPython interoperability, introduction of a new neural network abstraction, and the reorganization of existing abstractions for enhanced orthogonality and modularity.

## Application Level Semantics

### Motivation and Case For

### Abstraction Details

#### Arbitrary Computational Entry Point
#### Multi User Assumption
#### Cross Execution Persistance Model
#### Late Binding of Calls
#### Code-Spatial Modularity and Live Replacement
#### Language Level Compute Scale Agnosticism
## Data-Spatial Programming Model and Abstractions
### Motivation and Case For

One of Jaseci's key contribution is in the support of a new programming model called data-spatial programming. This paradigm has the potential to revolutionize the way problems are approached and solved by visualizing code execution in close proximity to data. It encourages programmers to send code to data instead of the traditional approach of passing data temporally to fixed code blocks. The associated programming language, Jac, has been developed to facilitate the implementation of data-spatial programming concepts.

Data-spatial programming fundamentally alters the mindset required to solve problems in code. By envisioning code blocks, specifically those associated with the walker abstraction, as entities that can move to the data they need, the paradigm introduces a spatial dimension to programming. This departure from the conventional temporal passing of variables to functions/methods promotes a more intuitive and natural way of thinking.
In data-spatial programming, the programmer is encouraged to send code to data, rather than sending data to fixed code blocks. 

We believe this paradigm aligns more closely with our human intuition. For example, when we need to clean a house, we naturally visualize ourselves as the cleaner moving through various rooms and locations where cleaning is required. Here, the cleaner represents the code, and the rooms and locations represent the data. Similarly, we instinctively collect and move objects around the house to organize or improve it. Data-spatial programming leverages these cognitive processes and incorporates them into the programming model through a number of Key Abstractions. 

#### Key Abstractions

To enable data-spatial programming, Jaseci and Jac introduce four key abstractions: walkers, nodes, edges, and abilities. These abstractions capture the essence of the paradigm and provide the necessary building blocks for implementing data-spatial programming concepts effectively.

1. **Walkers**: Walkers are the mobile entities in the data-spatial programming model. They represent the "cleaner" or code blocks that can move through the data, accessing and manipulating it as required. Walkers traverse the graph structure defined by nodes and edges, enabling a dynamic interaction with the data.

2. **Nodes**: Nodes are the fundamental units of data in the data-spatial programming model. They can be thought of as the "rooms" or locations that hold specific pieces of information or functionality. Walkers move between nodes to access and operate on the data contained within them.

3. **Edges**: Edges establish connections between "rooms" or nodes, forming a graph structure. They define the paths along which walkers can navigate. Edges determine the flow of execution and facilitate the movement of walkers between nodes.

4. **Abilities**: Abilities represent the capabilities or functions associated with either nodes and walkers. In our analogy, a cleaner may have a vacuum ability they can take to each room, and the washing machine may have a self-cleaning button the walker simply needs to push. Each node or walker may possess one or more abilities that walkers can leverage. Abilities define the actions that walkers can perform on the data within a node, allowing for dynamic and context-aware operations.

We submit, it is a lot stranger to think of passing rooms and locations to a fixed cleaning function and returning the cleaned room/location back to a caller. 

By combining these abstractions, Jaseci and Jac empower programmers to implement data-spatial programming effectively and leverage the inherent spatial and intuitive thinking processes for problem-solving. It's also important to note, there is a theoretical equivalence in programming expressivity of data-spatial programming to OOP or any other model. 

> **Important**
> 
> This data-spatial programming model is implemented to superset OOP, similar to how OOP is introduced to superset functional/procedural paradigm in C++/Python/Java etc. 

Data-spatial programming, as supported by Jaseci and its associated programming language Jac, introduces a novel paradigm that shifts the traditional temporal approach to code execution. By encouraging programmers to visualize code moving through data and sending code to data, data-spatial programming taps into our natural human intuition. The key abstractions of walkers, nodes, edges, and abilities form the foundation of this paradigm, enabling dynamic and context-aware interactions with data. With Jaseci and Jac, programmers can unlock new possibilities and explore problem-solving from a fresh perspective.

### Abstraction Details

#### Walkers
#### Nodes
#### Edges
#### Abilities
#### `here` and `visitor` Refs
#### Spawn Operator
#### Take Operator
#### Report Operator

## Full CPython Interoperability

A primary focus of Jaseci 2 is achieving full interoperability with CPython's abstractions. Jaseci will serve as a superset of CPython, allowing seamless integration with existing Python codebases. All novel Jaseci abstractions and concepts beyond Python will be represented using Python objects, ensuring compatibility and familiarity for Python developers. Similarly, Jaseci will support representation of all possible Python objects, maintaining a bidirectional compatibility between Jaseci and CPython.

## New Neural Network Abstraction

Jaseci 2 will introduce a new abstraction that represents a neural network model within the Jaseci runtime stack. This abstraction will build upon and extend the existing ONNX model standard and inference execution approach, providing a more generalizable and extensible framework. By leveraging the strengths of ONNX, Jaseci 2 ensures compatibility with various model types while enabling updates to fundamental compute patterns in a modular and orthogonal manner. The integration of this new abstraction enhances Jaseci's capabilities in machine learning and deep learning domains.

## Enhanced Orthogonality and Modularity

In Jaseci 2, all novel abstractions will be reorganized, simplified, and extended to enhance orthogonality and modularity. This reorganization aims to streamline the development process and improve the maintainability of codebases. Two specific examples of these changes include:

1. Naming Consistency: In Jaseci 2, all code blocks within walkers will be named abilities, aligning the syntax with nodes and edges. This resolves the inheritance issue and provides a uniform naming convention throughout the stack, making it easier for developers to reason about the code structure.

2. Edge Restructuring: Edges will transition from being classes to supersets of structs. They will no longer possess abilities, simplifying their implementation and reducing unnecessary complexity. This change enhances the clarity and modularity of the edge abstraction, allowing for more intuitive interactions and reducing the potential for conflicts.

These modifications to the existing abstractions in Jaseci 2 contribute to a cleaner and more cohesive programming model, enabling developers to work efficiently and effectively within the Jaseci ecosystem.

## Conclusion

Jaseci 2 retains its key data-spatial abstractions while providing full interoperability with CPython. It introduces a new neural network abstraction, building upon the ONNX standard, and enhances the orthogonality and modularity of all abstractions within the stack. These design choices ensure continuity, compatibility, and improved developer experience, empowering programmers to harness the power of data-spatial programming in a versatile and efficient manner.