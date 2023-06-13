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

The Purple Pill section delves into the newly introduced features in Jac that build upon and extend the current OOP / procedural model in Python. These enhancements are designed to make coding easier, more efficient, and more robust, thus improving the overall developer experience. This section provides an in-depth exploration of these innovative features and their practical applications.

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

spawner myspawner {} # define a spawner

can myfunc(): None {} # define a function

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
    b = len(a);
    print(b); }
```

#### Type System

While Python has dynamic typing with optional type hints, Jac takes it a small step further. Type hints in Jac are mandatory in function/method signatures and for object class member vairables. It's really not that much work, and provides key benefits of statically typed languages such as better code understanding, fewer programming errors and better performance. However, Jac still allows dynamic typing under the hood to be fully semantically interoperable with Python, and offer the pythonic flexibility of a dynamically typed language.

An additional benefit of this restrained strict type hinting is the potential for type inference. With type hints provided at critical junctures (function/method signatures and class member variables), Jac is designed to allow complete inference of types for non-hinted definitions within code blocks. This introduces a whole new realm of possibilities for the language in the long term. One such potential is the ability to transition into a C++ compatible language backend, enabling Jac to target C/C++ and further extending the utility and flexibility of Jac. However, it is crucial to note that this is a future aspiration; as of now, Jac remains deeply rooted in Python's syntax and semantics.

By blending the best aspects of static and dynamic typing, along with the potential for type inference, Jac positions itself as a versatile language that can adapt to different development needs while maintaining a strong tie to Python's design principles.

##### Minimal Code Example
```jac
"""Type hints aren't that much work."""

can foo(a: int, b: str): int {
    c = a + (b|>int);  # no type hint needed here
    return c;
}

object Bar {
    has a_list: list[int] = [1, 2, 3];
    has b_list: list[str] = ["5", "6", "7"];

    can init(): None {
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

    can init(a: int): None {
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
    priv: can init(a: int): None {
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
    priv: can init(a: int): None;
    pub: can set_a(val: int): None;
}

:o:MyObj:a:init {
        here.a = a;
}

:o:MyObj:a:set_a {
        here.a = val;
}
```
### Realizing Pythonic implemenations in a Jactastic way

Jac provides a comprehensive mapping of Python's core language features, ensuring Python developers can smoothly transition to Jac. At the same time, Jac introduces innovative modifications that enhance readability, explicitness, and flexibility, elevating the developer experience.


To ensure Jac provides a comprehensive coverage of Python's features, we provide analogous structures and functionalities for essential elements such as imports, global variables, free code at module level, Python-style function definitions, and Python-style class declarations, as well as a general mapping of code statements. Here, we detail these analogies.

### Imports in Jac, and Introducing Include

In Jac, the import system allows for two types of imports - 'jac' imports and 'py' imports, denoted as `import:jac ...` and `import:py ...` respectively. The syntax used for specifying the import paths is a direct mapping from the Python language's import syntax. This applies equally to both jac and py style imports. However, in Jac, the 'from' style imports have undergone a slight alteration, with the `name as new_name, ...` clauses being moved to the end of the sequence.

Also note that Jac's import system uses Python's `.` and `..` syntax for path specification in both jac and py style imports. This allows for consistency with existing Python syntax and understanding, and provides a seamless transition for developers familiar with Python's import system.

However, an important distinction lies in the elimination of wildcard imports like `from .mylib import *`, and its replacement with the `include` keyword. We view wildcarding as an issue of how to handle name visibility during standard imports. When a developer writes `include:jac .myjac;` or `include:py .mypy`, all element names within 'myjac' or 'mypy' are implicitly made available in the encompassing module. For instance, if an object named `Obj` exists within the included module, a developer can refer to `Obj` directly as `Obj` without the need to prefix it with `myjac.Obj`. Note however that the semantics of include are the same as import otherwise and do not behave like C/C++ includes. That is to mean a module is "executed" upon an include as with an import.

This introduction of `include` alongside `import` promotes ease of use and cleaner syntax when dealing with imported modules. This nuanced flexibility aligns with Jac's philosophy of providing explicit and intentional programming syntax while still maintaining the familiarity of Python conventions.

#### Minimal Code Example

```jac
"""You can import python modules freely."""

import:py random;
import:py from math, sqrt as square_root;  # list of as clauses comes at end
import:py datetime as dt;
include:jac .main_defs;  # includes are useful when brigning definitions into scope
import:jac from .lib, jactastic;

with entry {  # code that executes on module load or script run
    random_number = random.randint(1, 10);
    print("Random number:", random_number);
    # or, f"Random Number: {random_number}" |> print;

    s_root = square_root(16);
    print("Square root:", s_root);
    # or, f"Square root: {s_root}" |> print;

    current_time = dt.datetime.now();
    print("Current time:", current_time);
    # or, f"Current time: {current_time}" |> print;

    jactastic.Jactastic() |> print;
}
```

### Global Variables in Jac

In Jac, global variables are indicated using the `global` keyword. Similar to Python, these globals can be defined anywhere within the module. However, Jac was created with an emphasis on clarity and intentional programming; thus, globals must be explicitly marked with the `global` keyword to ensure that developers are conscious of their decision to use a global scope, thereby preventing potential conflicts and misunderstandings.

Supplementing the clear-cut design of Jac is the introduction of the global reference operator. With the potential for both global and local variables to share identical names, confusion may arise during code execution. To prevent this, the global reference operator can be used to unambiguously indicate that a global variable is being referred to.

The global reference operator in Jac can be represented in two equivalent forms, either `:global:` or `:g:`. When a variable name is surrounded by this operator, it is a clear indication that the variable in question is a global one.

Consider a scenario where you have a local and a global variable, both named `age`. If you simply call `age` in your code, it might be unclear or ambiguous whether you are referring to the local or global variable. However, by using the global reference operator `:global:age` or `:g:age` it becomes clear that you are explicitly referring to the global variable `age`.

This addition strengthens Jac's philosophy of explicitness and intentionality. It allows developers to maintain clarity in their codebase, preventing potential bugs caused by scoping issues, and promoting a high level of code readability.
#### Minimal Code Example

```jac
"""Globals are explicitly defined."""

global age = 25, temperature = 98.6, name = "John Doe";
global fruits = ["apple", "banana", "orange"];
global person = {"name": "Alice", "age": 30, "city": "New York"};

can print_globs(): None {
    age = 30;
    fruits = ["pear", "grape", "kiwi"];
    print(:g:age, temperature, name);  # :g:<name> references global vs local
    :global:fruits |> print;  # :g: and :global: are equivalent
    person |> print;
}
```

### Module Level Free Coding in Jac

In Jac, the use of a `with entry {}` code block is designed to encapsulate free code. Free code is code that is not encapsulated within a function or method, allowing it to be executed at the global level of a program.

These `with entry {}` blocks can be utilized multiple times within a module, similar to how Python allows interspersed code statements along with functions and classes. Although Jac provides the flexibility of having multiple blocks, it is recommended to maintain a single `with entry {}` block for the sake of clarity and readability. An issue with Python is it does not dissuade excessive scattering of free code in a module that can lead to a fractured codebase, making the code harder to understand and maintain.

In Jac, even though the language permits free code, caution is strongly encouraged when deciding where and when to use these blocks. We view the `with entry {}` approach as an important improvement upon free code in pyton. It adds an additional layer of organization and readability. This results in a cleaner code base by providing a clear demarcation of code that is meant to be executed at the global level. This not only promotes the clarity of intention but also assists in maintaining a neat and tidy code structure. This is consistent with Jac's philosophy of facilitating clean, comprehensible code and explicit programming practices.

#### Minimal Code Example
```jac
"""Organized free coding at module level."""

object Obj1 {
    has var: int;
    can init {
        here.var = 1;
    }
}

# with entry {  # allowed but discouraged
#    o1 = spawn Obj1; o1::init;
# }

object Obj2 {
    has var: int;
    can init {
        here.var = 2;
    }
}

# with entry {  # allowed but discouraged
#     o2 = spawn Obj2; o2::init;
# }

object Obj3 {
    has var: int;
    can init {
        here.var = 3;
    }
}

# with entry {  # allowed but discouraged
#     o3 = spawn Obj1; o3::init;
# }

with entry {
    o1 = spawn Obj1; o1::init;
    o2 = spawn Obj2; o2::init;
    o3 = spawn Obj3; o3::init;
    print(o1.var);
    print(o2.var);
    print(o3.var);
}
```
### Functions in Jac

In the Jac programming language, the `can` keyword is used in place of Python's `def` to declare a function, followed by the function's name, maintaining a structure similar to Python. Though the data spatial programming model doesn't need functions, the design decision to have these "module level can's" allows Python developers to transition to Jac smoothly, as the semantics and structures of Python's function definitions remain largely identical.

One unique aspect of function handling in Jac is the introduction of `has` variables along with pythonic variable definitions. These variables behave similarly to static variables in languages like C/C++, Java, and C#. Unlike other variables that are reinitialized every time a function is called, a `has` variable retains its value between function calls, making it a valuable tool for certain programming tasks. Python does not natively support this concept of static variables, Jac rectifies this gap.

Jac functions follows Python's dynamic typing approach inside the function's body. No type hints are required here. However, Jac does make type hints mandatory for function parameters to ensure type safety at function boundaries. Also, the type of the return value is required to be indicated in the function's signature. As an aside, A nice property of this approach is all variable types within functions are perfectly inferable, allowing strongly typed semantics without type specification in the body of the function and interestingly creating a foundation for new and interesting type semantics, though that is for future work.

It is important to note that unlike Python, Jac does not support returning multiple values directly in its return statement. From our perspective, this design choice enhances readability by reducing potential ambiguities. Instead of returning multiple values, we suggest wrapping these values in a collection object like a list, tuple, set, or dict, depending on the use case. This aligns with Jac's aim to provide a more explicit, intuitive, and efficient programming experience.



#### Minimal Code Example

```jac
"""Functions in Jac."""

can factorial(n: int): int {
    if n == 0 { return 1; }
    else { return n * factorial(n-1); }
}

can factorial_recount(n: int): int {
    has count = 0;  # static variable, state kept between calls
    count += 1 |> print;  # += is a walrus style operator in Jac
    if n == 0 { return 1; }
    else { return n * factorial(n-1); }
}
```
### Classes in Jac

In Jac, pythonic class declarations take on a slightly different syntax compared to Python, using the `object` keyword as opposed to `class`. This `object` notion along with a few others are key primitives in Jac's unique data spatial programming approach and capable of embodying various data spatial semantics. However, it also fully subsumes and maps to Python's class semantics so we discuss `object`s through this lens here. Later we'll delve into `object`s through a data spatial lens.

#### Constructor, spawning, self referencing, and access modifiers
A slight departure from Python is the replacement of the `__init__` method with simply `init` in Jac. This `init` method serves as the constructor function in a Jac object, initiating the object's state. `init` can be made private using the `priv` keyword.

Jac introduces a robust system of access modifiers, unlike Python which relies on the `_` and `__` conventions. Jac's 'priv', 'prot', and 'pub' keywords provide explicit control over access levels to the properties and methods of an object. These keywords represent private, protected, and public access modifiers respectively, providing a level of encapsulation more akin to other languages such as C++ or Java.

 There is also no need to specify the `self` keyword in method signatures. This has always felt awkward and redundant in Python. Instead, Jac implies its presence and uses of the `here` keyword to refer to the enclosing object instance.


```jac
"""Basic class implementation and spawning example."""

object Person {
    prot: has age: int;  # no need ot use `_age`
    pub: has name: str;

    priv: can init(name: str, age: int): None {
        here.name = name;
        here.age = age;
    }

    pub: can greet(): None {  # public is default if `pub` is not specified
        print("Hello, my name is ", here.name, " and I'm ", here.age, " years old.");
    }
}

with entry {
    my_guy = Person("John", 42);
    my_guy.greet();
}
```

In this example, we have a `Person` object with two properties: `name` and `age`. The `prot` keyword before `age` indicates that `age` is a protected property (only visible to it's class members and sub class members). Similarly, the `pub` keyword before `name` indicates that `name` is a public property (can be accessed via `.name` everywhere).

The constructor function is declared using `priv: can init(name: str, age: int): None`. This `init` function initializes the `Person` object's state. The `priv` keyword denotes that `init` is a private method, meaning it can only be accessed within the `Person` object. The method takes two arguments: `name` and `age`.

Inside the `init` method, we use the `here` keyword instead of `self`, which is traditionally used in Python. The `here` keyword refers to the instance of the `Person` object being manipulated, similar to how `self` works in Python.

Next, we have the `greet` method, which is a public method as denoted by the `pub` keyword. This method prints a greeting message using the `name` and `age` properties.

By switching from `self` to `here`, and from `__init__` to `init`, Jac brings a cleaner and more straightforward syntax for defining and initializing objects. With the introduction of access modifiers (`priv`, `prot` and `pub`), Jac provides a more robust system than `_` and `__` for encapsulating properties and methods within an object, aligning closer to other languages such as C++, Java, and C#. At the same time its all optional and up to the developer if they'd like a more pythonic less pedantic style ot implementation as per:

```jac
"""A bit more chill approach."""

object Person {
    has age: int, name: str;

    can init(name: str, age: int): None {
        here.name = name;
        here.age = age;
    }

    can greet(): None {
        print("Hello, my name is ", here.name, " and I'm ", here.age, " years old.");
    }
}

with entry {
    Person("John", 42).greet();
}
```
#### Inheritance

Inheritance is a fundamental principle of object-oriented programming that allows one class (or `object` in Jac) to inherit the properties and methods of another. This helps promote code reusability and can lead to a more logical, hierarchical object structure.

Similar to Python, Jac allows for both single and multiple inheritance. Here's how you might define a simple single inheritance scenario:

```jac
"""Super simple example of inheritance."""

object Parent {
    can init(): None {
        # Parent initialization
    }
    can speak(): None {
        # Parent speaking
    }
}

object Child:Parent {
    can init(): None {
        # Child initialization
        :o:Parent.init();  # Initialize parent, :o: is alias for :object:
    }
}
```

In this example, `Child` is a subclass of `Parent` and inherits all properties and methods of `Parent`. This means instances of `Child` can also invoke the `speak()` method.

Multiple inheritance, a concept where a class can inherit from more than one superclass, is also supported:

```jac
"""Example of multiple inheritance."""

object Parent {
    can init(): None {
        # Parent initialization
    }
    can speak(): None {
        # Parent speaking
    }
}

object Mom:Parent {
    can init(): None {
        # Mom initialization
        :o:Parent.init();
    }
    can calm(): None {
        # Mom speaking
    }
}

object Dad:Parent {
    can init(): None {
        # Dad initialization
        :o:Parent.init();
    }
    can excite(): None {
        # Dad speaking
    }
}

object Child:Mom:Dad { #Child inherits from Mom and Dad
    can init(): None {
        # Child initialization
        :o:Mom.init();
        :o:Dad.init();
    }
}
```

In this case, `Child` is a subclass of both `Mom` and `Dad` and inherits all their methods. Therefore, instances of `Child` can invoke both `calm()` and `excite()` methods.

When it comes to method overriding (i.e., a subclass providing a different implementation of a method already defined in its superclass), the subclass can simply define the method with the same name. If the method is called on the subclass, Jac will prioritize its own implementation over the inherited one.

Furthermore, if a method in a superclass needs to be invoked from the subclass, it can be done using the object reference op `:o:` and the particular object type name, following the same convention as in Python. Super() is less explicit and potentially confusing so its not present in Jac at the moment (though this is under consideration for future versions).

These inheritance semantics enable Jac to utilize the powerful constructs of object-oriented programming, providing a familiar and flexible paradigm for Python developers.


### Exception Handling in Jac

Jac Exceptions build directly upon Python's exceptions including `try`, `except`, `finally` and `raise` keywords using the same semantics (and imported Exception objects) as python. Jac also imports Python's hierarchy of exceptions with base class `Exception` and supporting the various built-ins like `IOError`, `ValueError`, `TypeError`, `IndexError`, and `KeyError`, etc. Users can define their own exceptions by creating a new subclass of the `Exception` class or any of its descendants.

The `try` block wraps around a section of code for which exceptions will be checked. If an exception is raised in the `try` block, the flow of control immediately passes to an appropriate `except` block that handles that exception. If no exception is raised, the `except` blocks are skipped.

Multiple `except` clauses can be defined to handle various types of exceptions. Each `except` clause specifies the type of exception it handles, and if an exception of that type or a subtype thereof is raised in the `try` block, that `except` clause handles it. An `except` clause with no exception type specified will catch all exceptions that are not caught by an earlier `except` clause.

The `finally` keyword is used for specifying actions that must be executed regardless of whether an exception was raised or not. Code under the `finally` block will always execute after the `try` and `except` blocks, even if they include a `return`, `continue`, or `break` statement, or if an exception is raised that isn't caught.

The `raise` keyword is used to trigger an exception manually and can be followed by the name of the exception to be raised.

#### Minimal Code Example

```jac
"""Exception example in Jac."""

can divide_numbers(a: float, b: float): float {
    try {
        result = a / b;
    }
    except ZeroDivisionError as e {
        print("Error: Cannot divide by zero!", e);
        result = None;
        raise;  # Re-raise the exception
    }
    finally {
        print("Division operation completed.");
    }
    return result;
}

with entry {
    try {
        numerator = int(input("Enter the numerator: "));
        denominator = int(input("Enter the denominator: "));
        result = divide_numbers(numerator, denominator);
        print("Result:", result);
    }
    except ValueError {
        print("Error: Invalid input! Please enter valid integers.");
    }
}
```

### Code Statements amd Expressions in Jac

For general code statements and expression, we provide an equivalency set that mirrors Python's structures. We've also expanded on the capabilities described here with the new language features that add additional functionality and flexibility to the Jac programming language. These are discussed in the next section (Purple Pill). Here we describe the basic equivalency set.

#### Complete Set

##### Assignment

```jac
a = 8+foo(9);
```

##### Expressions

```jac
data[5+3].foo(9);
```
##### Walrus (expanded)

```jac
a := b := 5;
```

##### Walrus (expanded set, introduced in Jac)
```jac
a += b *= 5 /= c;
```

##### If, Elif, Else
```jac
if a > b {print("a is greater than b");}
elif a < b {print("a is less than b");}
else {print("a is equal to b");}
```
##### For Loops
```jac
for fruit in ["apple", "banana", "cherry"] {fruit|>print;}
```

##### Iteration For Loops (introduced in Jac)
```jac
for i=0 to i<100 by i+=1 {i|>print;}
```
##### While Loops
```jac
i = 100;
while i {
    i|>print;
    i-=1;
}
```

##### Asserts
```jac
assert(mem_left!=0);
```

##### Control (Continues, Breaks)
```jac
for i=0 to i<100 by i+=1 {i|>print; if(i<50) {break;}}
```

##### Delete
```jac
delete mylist[4];
```

##### Return
```jac
return "I completed";
```

##### Yield
```jac
yield i-2;
```

##### Multistrings
```jac
output = "the first "
         "and then second";
```

##### F-strings
```jac
output = f"i can do math {1+1}";
```



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

This section of the Jac language specification dives into the composition of how the data spatial programming model is achieved through Jac's four primary architypes: objects, nodes, edges, and walkers. These architypes represent various categories of the notion of a traditional class, each with its unique traits and functionalities.
### Main Components of an Architype in Jac

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


### The Node Architype
### The Edge Architype
### The Walker Architype
### The Object Architype
### Computation via Traversing Graphs
### Data In-Situ Programming
### Report
### Yield
### Cross Invocation Persistence
### The Sentinel
