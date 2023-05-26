---
sidebar_position: 1
description: Jaseci 2.0 Architecture
title: Architecture of Jaseci
---

# Jaseci 2 Design Specifications

## Introduction

Jaseci 2 is the next version of the computational runtime stack, designed to support data-spatial programming and provide a seamless integration with CPython. This document outlines the key features and changes in Jaseci 2, including the retention of novel data-spatial abstractions, full CPython interoperability, introduction of a new neural network abstraction, and the reorganization of existing abstractions for enhanced orthogonality and modularity.

## Data-Spatial Abstractions

Jaseci 2 will retain its key novel data-spatial abstractions, namely nodes, edges, walkers, and abilities. These abstractions enable a shift in the programmer's mindset towards in-situ compute, where code and data are tightly coupled. By expressing all computations through near-data operations on a graph, code can move through the graph spatially, resulting in efficient and intuitive programming. The preservation of these abstractions ensures continuity with the previous version and maintains the core principles of data-spatial programming.

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