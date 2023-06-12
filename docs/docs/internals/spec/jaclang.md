---
sidebar_position: 3
description: Full Spec of Jac Language
title: Jac Language Specification
---

# Jac Programming Language Specification


## Module Structure

### General Organization

In the Jac programming language, the fundamental organizational unit of code is the "module". Each Jac module is a coherent assembly of various elements, which we term "architypes". The modular design is intended to encourage clean, well-structured, and maintainable code.

#### Architypes

The term "architype" is a distinct concept in the data spatial programming paradigm. It represents several classes of traditional classes, each carrying unique semantics. In Jac, an architype can take one of the following forms:

1. **Object Types**: Traditional classes, as seen in Object-Oriented Programming (OOP), form the foundation of Jac's object types. They are responsible for encapsulating data and the operations that can be performed on that data.

1. **Node Types**: Node types define the structure of individual nodes in the data space. They detail the properties and data that a node can hold. Node types, along with edge adn walker types can seen as variations of object types that have different semantics.

1. **Edge Types**: Edge types establish the semantics of the connections between nodes. They specify the nature of the relationship, including any constraints or properties associated with the edge.

1. **Walker Types**: Walker types encapsulate the logic for navigating the data space. They can be seen as agents that traverse nodes and edges to perform operations or gather information.

#### Additional Module Elements

Beyond the key architypes, a Jac module incorporates several additional element components, the complete list includes:

1. **Abilities Definitions**: Abilities can manifest as either traditional OOP-style methods or data spatial-specific abilities. These abilities give object types, node types, edge types, and walker types the capacity to perform tasks or computations.

1. **Spawners**: Spawners are like functions but with a data-spatial twist. They execute and return values like function however instead of taking parameters, spawners are sent to the data they need to process and leverage a duck typing philosophy to their execution. They can be thought of as mobile computation units that are dispatched to data elements, and the can be spawned on any type including, objects, dictionaries, lists, etc.

1. **Import Directives**: Import directives provide the mechanism for reusing code across different modules. They enable a module to incorporate functionalities defined in other modules, fostering code reusability and modularity.

1. **Global Variable Definitions**: Global variables can be declared and defined within a module. These are accessible throughout the module's scope. However, Jac's design philosophy mildly discourages extensive reliance on globals. This discouragement stems from a desire to enhance modularity and encapsulation, promote code readability, and support codebase scalability. Overuse of global variables can lead to tightly coupled, less maintainable code.
    1. Note: While Jac provides the ability to declare global variables, developers are urged to exercise this power sparingly. Overdependence on global variables often results in code that is hard to debug, difficult to understand, and not modular, reducing the scalability of the codebase. Instead, the Jac language promotes encapsulation and modular design through its architype and abilities system, leading to cleaner, more maintainable, and scalable code.

1. **Test Definitions**: In line with best practices for software development, Jac modules can contain test definitions. These tests provide an automated way to validate the behavior of architypes, abilities, and other components within a module. They form a key part of the development cycle, enabling continuous validation and refactoring of code with confidence. Test definitions can be structured in a variety of ways, including unit tests for individual components, integration tests to verify interoperability, and end-to-end tests to validate system-wide behavior.

#### Minimal Code Example

The following code example shows all elements that form a Jac module.

```jac
"""
A
Docstring
"""

global ver = "0.0.1";  # global variable

import:jac .utils;  # import a module

object mytype {}  # define a new type

node mynode:this:that {}  # define a new node

edge parent {}  # define a new edge

walker travelor {  # define a new walker
    can say_hello;
}

:walker:travelor:ability:say_hello {
    "Hello" |> print;  # |> is a pipe forward operator
}

spawner myspawner {} # define a new spawner

func myfunc(): None {} # define a function

test mytest
"A test of my functionality" {
   # test code here
}
```

### Emphasizing Declarations and Definitions in Jac

In the pursuit of more organized, scalable, and readable codebases, the Jac programming language revives the distinction between ability declarations and definitions. This approach is a deviation from Python, which do not explicitly separate method definitions from their declarations.

In Jac, a declaration refers to announcing the existence and signature of an ability to an object type, node type, edge type, or walker type. A declaration specifies the name and either data spatial event details, or method parameters and return details of an ability, but does not detail the actual implementation or behavior. On the other hand, a definition provides the complete description of the declared element, detailing how it operates or behaves. This can be specified within the same Jas module file, or in a separate module file.
#### Minimal Code Example
`main.jac`
```jac
import:jac .defs

walker travelor {
    can say_hello with entry;  # data spatial ability declared
    can say_whatever(msg: str);  # traditional method declared

    # inline ability definition (python only supports this)
    can say_goodbye {
        "Goodbye" |> print;
    }
}
```

`defs.jac`
```jac
:walker:travelor:ability:say_hello {
    "Hello" |> print;  # |> is a pipe forward operator
}

# :w: and :a: are aliases for :walker: and :ability:
:w:travelor:a:say_whatever(msg: str) {
    msg |> print;
}
```

The benefits of this separation are manifold:

1. **Readability**: By separating the declaration from the definition, developers can easily understand what an element does just by looking at its signature, without getting lost in the details of its implementation.

2. **Organizational Clarity**: Declarations serve as an overview or table of contents for a module, making it easier to understand the module's structure and functionalities at a glance.

3. **Scalability**: The distinction allows for improved code organization in larger codebases. A module can contain declarations that are defined in different parts of the program, allowing for better distribution of code.

4. **Improved Debugging and Maintenance**: This approach makes debugging easier as it provides a clear distinction between interface and implementation. If a bug occurs, it is more straightforward to identify whether it's due to a faulty implementation or a misuse of the interface.

The reintroduction of this distinction in Jac reflects a philosophy of design clarity and software robustness. By encouraging developers to think about the interface of their code separate from its implementation, Jac promotes the development of clear, maintainable, and scalable software.

## Main Architypes of Jac

This section of the Jac language specification dives into the composition of its four primary architypes: objects, nodes, edges, and walkers. These architypes represent various categories of traditional class notions, each with its unique traits and functionalities.

### General across all Architype

Across all architypes in Jac, there are three main types of fields: has variables, data spatial abilities, and method abilities.

#### Has Variables

Has variables stand for the variable fields of the architype. Unlike other elements of the Jac language, these fields are strongly typed, thereby requiring explicit type declaration. This ensures that each has variable adheres to a specific type, promoting a sense of robustness and predictability within the language, even while other areas of code allow for dynamic type inference.

#### Data Spatial Abilities

Data spatial abilities, on the other hand, are akin to methods in other languages but imbued with the distinct semantics of data spatial programming. These abilities do not operate on traditional parameter passing or value returning paradigms. Instead, all data access is facilitated exclusively through two references: `here` and `visitor`.

- The `here` reference allows access to the has fields of the node or object that a walker is currently visiting. This visitation-based data access highlights the unique traversal mechanics of Jac's data spatial model.

- The `visitor` reference only provides access to the has variables of the walker itself. It is through this constraint that data sharing between the visited node or object (`here`) and the walker (`visitor`) is permitted.

This spatial ability to access and manipulate data, unique to Jac, aligns with the spatial model of data programming, thus strengthening its differentiating edge.

#### Method Abilities

Method abilities are reminiscent of traditional class methods in other programming languages. They accept parameters and return values, providing a more conventional programming mechanism within Jac. However, just like has variables, these parameters and return types must also be explicitly defined. This requirement ensures type safety during method invocation, helping to prevent runtime errors.

## Summary

In conclusion, each of Jac's architypes—object types, node types, edge types, and walker types—possesses these three main field types: has variables, data spatial abilities, and method abilities. This innovative blend of strict typing for variables and methods, along with data spatial programming concepts, forms the crux of Jac's robust and unique programming model. The interplay between the `here` and `visitor` references further accentuates Jac's commitment to facilitating a dynamic and intuitive data spatial programming experience.
