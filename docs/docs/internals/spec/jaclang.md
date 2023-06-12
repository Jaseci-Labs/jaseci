---
sidebar_position: 3
description: Full Spec of Jac Language
title: Jac Language Specification
---

# Jac Programming Language Specification

This document serves a dual purpose. It provides an introductory guide to understanding the Jac programming language and also offers a full specification of its features, conventions, and best practices.

The document is organized into several distinct parts, each covering a different aspect of the language to provide a comprehensive overview of Jac.

## Structure of the Document

The specification begins with a discussion of the general structure of a Jac module and an overview of code organization principles. This section will provide a broad understanding of how Jac programs are structured and organized.

Following the introduction, the document is divided into three main parts: The Blue Pill, The Purple Pill, and The Red Pill specifications.

### The Blue Pill Specification

The Blue Pill section covers the features of Jac that have a direct one-to-one mapping with Python. This section aims to illustrate how typical Python solutions can be implemented in a 'Jactastic' way. By examining these parallels, Python programmers transitioning to Jac can gain a deeper understanding of Jac’s unique characteristics, while leveraging their existing knowledge of Python.

### The Purple Pill Specification

The Purple Pill section delves into the newly introduced features in Jac that build upon and extend the current OOP model in Python. These enhancements are designed to make coding easier, more efficient, and more robust, thus improving the overall developer experience. This section provides an in-depth exploration of these innovative features and their practical applications.

### The Red Pill Specification

The Red Pill section provides a thorough examination of the language features related to the innovative data spatial programming model. This part of the document covers the new set of semantics and concepts that Jac realizes and provides examples and explanations on how these features can be used in data spatial programming. This exploration will provide a comprehensive understanding of this groundbreaking programming model and its advantages.

By exploring each of these sections, readers can gain a thorough understanding of Jac, its similarities and differences with Python, its innovative features, and the benefits of data spatial programming.

## General Overview of a Jac Module

### Code Organization

In the Jac programming language, the fundamental organizational unit of code is the "module". Each Jac module is a coherent assembly of various elements, which we term "architypes". The modular design is intended to encourage clean, well-structured, and maintainable code.

#### Architypes

The term "architype" is a distinct concept in the data spatial programming paradigm. It represents several classes of traditional classes, each carrying unique semantics. In Jac, an architype can take one of the following forms:

1. **Object Types**: Traditional classes, as seen in Object-Oriented Programming (OOP), form the foundation of Jac's object architypes. They are responsible for encapsulating data and the operations that can be performed on that data.

1. **Node Types**: Node types define the structure of individual nodes in the data space. They detail the properties and data that a node can hold. Node types, along with edge adn walker types can seen as variations of object types that have different semantics.

1. **Edge Types**: Edge types establish the semantics of the connections between nodes. They specify the nature of the relationship, including any constraints or properties associated with the edge.

1. **Walker Types**: Walker types encapsulate the logic for navigating the data space. They can be seen as agents that traverse nodes and edges to perform operations or gather information.

#### Additional Module Elements

Beyond the key architypes, a Jac module incorporates several additional element components, the complete list includes:

1. **Import Directives**: Import directives provide the mechanism for reusing code across different modules. They enable a module to incorporate functionalities defined in other modules, fostering code reusability and modularity.

1. **Functions**: Traditional functions, these represent the basic standard python `def` style function which can include input parameters and return a value.

1. **Module Level Free-Style Code**:  "Free Style" code at the module level refers to executable code that is not encapsulated within a function or class. This code is executed when the module is imported or run as a script, making it ideal for initializing module-level variables or running setup tasks.
    1. Note: However, we recommended to limit its usage to improve readability and maintainability of the code. We also enforce explicit specification of this with a module level `with entry {}` directive.

1. **Abilities Definitions**: Abilities can manifest as either traditional OOP-style methods or data spatial-specific abilities. These abilities give object types, node types, edge types, and walker types the capacity to perform tasks or computations.

1. **Spawners**: Spawners are like functions but with a data-spatial twist. They execute and return values like function however instead of taking parameters, spawners are sent to the data they need to process and leverage a duck typing philosophy to their execution. They can be thought of as mobile computation units that are dispatched to data elements, and the can be spawned on any type including, objects, dictionaries, lists, etc.


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

with entry {
    # module level freestyle code
}

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



## Blue Pill: Jac Mapping to Python Semantics and Syntax

Jac is a data spatial programming language that goes beyond Python in several key ways. However it is a superset language semantically, so lets start with understanding Jac through the lens of how typical python style implementation is realized.

### General blue-pill tier differences / improvements over Python

While Python has been widely lauded for its readability and simplicity, Jac introduces several new features and structures that are aimed at providing even greater control, predictability, and flexibility to developers.

#### Whitespace Doesn't Matter

Unlike Python, where whitespace and indentations are crucial for the structure of the code, Jac relaxes these restrictions. Whitespace in Jac does not dictate code blocks; instead, the language reintroduces braces `{}` and semicolons `;` to delineate blocks and terminate lines respectively, reminiscent of many C-style languages. This allows code to be more compact when desired and offers flexibility in styling.

While Python places strong emphasis on the usage of whitespace and indentations for denoting the structure of the code, Jac has a more flexible approach. In Python, these strict formatting rules can occasionally lead to less concise code and even impede the readability of the code in certain scenarios. In Jac, the emphasis on whitespace does not exist, providing more freedom and flexibility to developers. This approach permits developers to create more compact and versatile code, while preserving the clarity and understandability of the code.

That being said, Jac acknowledges the value of the Python's black package, a code formatting tool that strictly enforces a uniform (and opinionated) standard code structure across a project, thereby enhancing a particular approach readability and maintainability. Thus, Jac has built this concept into the core of the language stack itself, offering a standardized auto-formatting tool as an optional feature. This feature provides the benefit and tooling for PEP8 style conventions to create clean, structured, and consistent code across all projects. By integrating strict coding standards via black-style tooling while allowing for flexibility for developer choice, we believes this strikes the perfect balance for a language.

##### Minimal Code Example

```jac
"""Same functionality 3 white space styles."""

with entry { "hello" |> len |> print; }  # more concise

with entry {  # a bit more python like
    a = "hello" |> len;
    a |> print;
}

with entry {  # very pythonic
    a = "hello";
    b = len("hello");
    print(b); }
```

#### Typing System

While Python has dynamic typing with optional type hints, Jac takes it a small step further. Type hints in Jac are mandatory in function/method signatures and for object class member vairables. It's really not that much work, and provides key benefits of statically typed languages such as better code understanding, fewer programming errors and better performance. However, Jac still allows dynamic typing under the hood to be fully semantically interoperable with Python, and offer the pythonic flexibility of a dynamically typed language.

An additional benefit of this restrained strict type hinting is the potential for type inference. With type hints provided at critical junctures (function/method signatures and class member variables), Jac is designed to allow complete inference of types for non-hinted definitions within code blocks. This introduces a whole new realm of possibilities for the language in the long term. One such potential is the ability to transition into a C++ compatible language backend, enabling Jac to target C/C++ and further extending the utility and flexibility of Jac. However, it is crucial to note that this is a future aspiration; as of now, Jac remains deeply rooted in Python's syntax and semantics.

By blending the best aspects of static and dynamic typing, along with the potential for type inference, Jac positions itself as a versatile language that can adapt to different development needs while maintaining a strong tie to Python's design principles.

##### Minimal Code Example
```jac
"""Type hints aren't that much work."""

func foo(a: int, b: str): int {
    c = a + (b|>int);  # no type hint needed here
    return c;
}

object Bar {
    has a_list: list[int] = [1, 2, 3];
    has b_list: list[str] = ["5", "6", "7"];

    can entry(): None {
        for i in here.b_list {
            foo(5, i) |> print;
        }
    }
}
```
#### Improving on the class `self` reference

In Python, instance methods require the explicit mention of `self` as their first parameter for accessing instance data. This explicit declaration, although informative, can feel a little awkward and redundant to developers, especially given the language's propensity for clear and clean code.

Jac seeks to remedy this through introducing the `here` reference as s replacement as an implicit self-reference within each class method. This implicit reference is assumed in all methods, eliminating the need for developers to manually include it. The code thus becomes cleaner, more readable, and a bit more intuitive.

This alteration in Jac addresses a longstanding peculiarity in Python's object-oriented design. The repeated use of self in Python can seem a bit odd, particularly considering the language's dynamic nature. While Python utilizes self to ensure that instance methods have a way to access and modify instance data, Jac believes that this access can be assumed rather than explicitly stated, given the context of the method within a class.

Furthermore, Jac's approach aligns better with other object-oriented languages, where the current instance of the object within its methods is implicitly understood. By casting objects explicitly and assuming an implicit here reference, Jac simplifies method definitions and allows developers to focus on the logic of the method rather than the mechanics of accessing instance data.

##### Minimal Code Example
```jac
"""Not focusing on the self is cleaner."""

object MyObj {
    has a: int;

    can entry(a: int): None {
        here.a = a;
    }

    can set_a(val: int): None {
        here.a = val;
    }
}
```

#### OOP Access Modifiers

In Python, the visibility and access rights of class members are signified using a simple convention that employs the underscore (`_` and `__`). While this is a compact notation, it's often misunderstood and poorly enforced, leading to potential misuse and confusion. It can also appear as an afterthought or a makeshift solution, rather than a robust design choice.

Jac chooses to address this issue by incorporating explicit optional keywords to define class member visibility. The keywords `priv`, `prot`, and `pub` are used to indicate private, protected, and public access respectively. This is a more explicit and understandable approach, which significantly enhances code readability and clarity.

This enhancement is not just syntactical, but deeply semantic. The use of clear keywords provides predictability in class structure, making the classes easier to understand and maintain. The explicit nature of these keywords ensures developers have a precise understanding of the scope and accessibility of class members, leading to fewer mistakes and more efficient collaboration.

Moreover, the formal support for these accessors in Jac makes it straightforward to understand the structure and hierarchy o f class members, and the level of accessibility of each member. It's a simple yet significant shift that makes class designs more coherent and intuitive.

By transitioning from Python's underscore convention to the use of explicit keywords, Jac promotes predictability and readability, leading to a more structured and intuitive programming model.

##### Minimal Code Example
```jac
"""No more `_` and `__` for access/visibility directives."""

object MyObj {
    prot: has a: int;
    priv: can entry(a: int): None {
        here.a = a;
    }
    pub: can set_a(val: int): None {
        here.a = val;
    }
}
```

#### Definitions and Declarations

As previously mentioned, in Python, there is a direct tie between declarations and definitions. When you declare a function or a class, you inherently provide its definition. This conjoined approach can be efficient in certain contexts, but forcing this approach when dealing with larger code bases present readability and organizational challenges. Often, understanding the interface of a class or a function requires scrolling through lines of implementation details, or relying on IDE tools for quick summaries. This can make it difficult to get a comprehensive overview of the class or function structure.

Jac introduces a distinction between declarations and definitions, directly addressing this challenge. In Jac, a programmer can first declare the structure of a class, outlining its methods and member variables, and subsequently provide the definitions or implementation details. This separation improves code readability and organization by enabling a clear, high-level overview of the class or function structure before diving into the implementation specifics. If a programmer chooses to conjoin declaration and definition, they can also do that as well.

This approach is particularly beneficial in large projects where different team members may be working on different parts of a class or function. With the separation of declarations and definitions, developers can quickly understand the interface of a class or function without having to navigate through the implementation details. This leads to a better collaborative environment and more efficient development process.
##### Minimal Code Example
```jac
"""Modified for separate defs/decls."""

object MyObj {
    prot: has a: int;
    priv: can entry(a: int): None;
    pub: can set_a(val: int): None;
}

:o:MyObj:a:entry {
        here.a = a;
}

:o:MyObj:a:set_a {
        here.a = val;
}
```
### Realizing Pythonic implemenations in a Jactastic way

Jac provides a comprehensive mapping of Python's core language features, ensuring Python developers can smoothly transition to Jac. At the same time, Jac introduces innovative modifications that enhance readability, explicitness, and flexibility, elevating the developer experience.


To ensure Jac provides a comprehensive coverage of Python's features, we provide analogous structures and functionalities for essential elements such as imports, global variables, free code at module level, Python-style function definitions, and Python-style class declarations, as well as a general mapping of code statements. Here, we detail these analogies.

### Imports in Jac

In Jac, there are two kinds of imports: `jac` imports and `py` imports. The syntax for the import path maps directly to Python. However, for `name as` type imports, the syntax is slightly changed with the `as` clause coming at the end. This subtle shift aligns with Jac's design philosophy of explicitness and readability.

#### Minimal Code Example

### Global Variables in Jac

To specify global variables in Jac, we use the `global` keyword, similar to Python. However, in line with Jac's design philosophy, we view each global variable as an element floating in the module, reinforcing Jac's explicit approach to variable declaration and scope.

#### Minimal Code Example

### Module Level Free Coding in Jac

For free code, or code that is not inside a function or method, we use a `with import {}` code block. While multiple blocks can be used if desired, we recommend sticking to a single block for readability and clarity.

#### Minimal Code Example

### Function Definitions in Jac

Jac uses `func` instead of Python's `def` to declare a function. The function's name follows the `func` keyword, similar to Python's convention. The semantics and structure of function definitions are nearly identical to Python's, ensuring a seamless transition for Python developers.

#### Minimal Code Example

### Class Declarations in Jac

Class declarations in Jac use `object` instead of Python's `class`. The constructor function in Jac is declared using `can entry()` instead of Python's `__init__`. This shift aligns with Jac's innovative approach to object-oriented programming, while still maintaining familiarity for Python developers.

#### Minimal Code Example

### Exception Handling in Jac

Jac Exceptions build directly upon Python's exceptions. Jac includes `try`, `except`, `finally` and `raise` keywords using the same semantics (and imported objects) as python.

#### Minimal Code Example

### Code Statements amd Expressions in Jac

For general code statements and expression, we provide an equivalency set that mirrors Python's structures. We've also expanded on the capabilities described here with the new language features that add additional functionality and flexibility to the Jac programming language. These are discussed in the next section (Purple Pill). Here we describe the basic equivalency set.

#### Minimal Code Example



## Purple Pill: New Language Features to Improve Traditional Programming

### Pipe Forward Operator
### Null Safe Operators
### Elvis Operator
### Spawners
### Freestyle Spawn Contexts
### Freestyle Filter Contexts
### Enhanced Walrus Operations
### Dict Typing
### Duck Typing

## Red Pill: Concepts, Semantics, and Features for Realizing Data Spatial Programming

### Main Architypes of Jac

This section of the Jac language specification dives into the composition of its four primary architypes: objects, nodes, edges, and walkers. These architypes represent various categories of traditional class notions, each with its unique traits and functionalities.

Across all architypes in Jac, there are three main types of fields: has variables, data spatial abilities, and method abilities.

##### Has Variables

Has variables stand for the variable fields of the architype. Unlike other elements of the Jac language, these fields are strongly typed, thereby requiring explicit type declaration. This ensures that each has variable adheres to a specific type, promoting a sense of robustness and predictability within the language, even while other areas of code allow for dynamic type inference.

##### Data Spatial Abilities

Data spatial abilities, on the other hand, are akin to methods in other languages but imbued with the distinct semantics of data spatial programming. These abilities do not operate on traditional parameter passing or value returning paradigms. Instead, all data access is facilitated exclusively through two references: `here` and `visitor`.

- The `here` reference allows access to the has fields of the node or object that a walker is currently visiting. This visitation-based data access highlights the unique traversal mechanics of Jac's data spatial model.

- The `visitor` reference only provides access to the has variables of the walker itself. It is through this constraint that data sharing between the visited node or object (`here`) and the walker (`visitor`) is permitted.

This spatial ability to access and manipulate data, unique to Jac, aligns with the spatial model of data programming, thus strengthening its differentiating edge.

##### Method Abilities

Method abilities are reminiscent of traditional class methods in other programming languages. They accept parameters and return values, providing a more conventional programming mechanism within Jac. However, just like has variables, these parameters and return types must also be explicitly defined. This requirement ensures type safety during method invocation, helping to prevent runtime errors.

### Key new concept

Each of Jac's architypes—object types, node types, edge types, and walker types—possesses these three main field types: has variables, data spatial abilities, and method abilities. This innovative blend of strict typing for variables and methods, along with data spatial programming concepts, forms the crux of Jac's robust and unique programming model. The interplay between the `here` and `visitor` references further accentuates Jac's commitment to facilitating a dynamic and intuitive data spatial programming experience.
