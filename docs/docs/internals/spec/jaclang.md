---
sidebar_position: 3
description: Full Spec of Jac Language
title: Jac Language Specification
---

# Jac Programming Language Specification


## Module Structure

### Overview

In the Jac programming language, the fundamental organizational unit of code is the "module". Each Jac module is a coherent assembly of various elements, which we term "architypes". The modular design is intended to encourage clean, well-structured, and maintainable code. 

### Architypes

The term "architype" is a distinct concept in the data spatial programming paradigm. It represents several classes of traditional classes, each carrying unique semantics. In Jac, an architype can take one of the following forms:

- **Object Types**: Traditional classes, as seen in Object-Oriented Programming (OOP), form the foundation of Jac's object types. They are responsible for encapsulating data and the operations that can be performed on that data.

- **Node Types**: Node types define the structure of individual nodes in the data space. They detail the properties and data that a node can hold.

- **Edge Types**: Edge types establish the semantics of the connections between nodes. They specify the nature of the relationship, including any constraints or properties associated with the edge.

- **Walker Types**: Walker types encapsulate the logic for navigating the data space. They can be seen as agents that traverse nodes and edges to perform operations or gather information.

### Additional Module Elements

Beyond the key architypes, a Jac module incorporates several additional components:

- **Abilities Definitions**: Abilities can manifest as either traditional OOP-style methods or data spatial-specific abilities. These abilities give object types, node types, edge types, and walker types the capacity to perform tasks or computations.

- **Import Directives**: Import directives provide the mechanism for reusing code across different modules. They enable a module to incorporate functionalities defined in other modules, fostering code reusability and modularity.

- **Global Variable Definitions**: Global variables can be declared and defined within a module. These are accessible throughout the module's scope. However, Jac's design philosophy mildly discourages extensive reliance on globals. This discouragement stems from a desire to enhance modularity and encapsulation, promote code readability, and support codebase scalability. Overuse of global variables can lead to tightly coupled, less maintainable code.
  - Note: While Jac provides the ability to declare global variables, developers are urged to exercise this power sparingly. Overdependence on global variables often results in code that is hard to debug, difficult to understand, and not modular, reducing the scalability of the codebase. Instead, the Jac language promotes encapsulation and modular design through its architype and abilities system, leading to cleaner, more maintainable, and scalable code.

- **Test Definitions**: In line with best practices for software development, Jac modules can contain test definitions. These tests provide an automated way to validate the behavior of architypes, abilities, and other components within a module. They form a key part of the development cycle, enabling continuous validation and refactoring of code with confidence. Test definitions can be structured in a variety of ways, including unit tests for individual components, integration tests to verify interoperability, and end-to-end tests to validate system-wide behavior.

### Minimal Code Example

