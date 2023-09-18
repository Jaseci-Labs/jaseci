# General Overview of a Jac

Jac programs are organized as a set of modules. A Jac module, at its core, is a logical and functional unit of code organization in the Jac programming language and semantically maps to the notion of a Python Module. The  module contains definitions for elements such as global variables, functions, and object types (classes), and can be imported and utilized in other modules. However, Jac reimagines a few traditional constructs and incorporates a number of new constructs and semantics in realizing its innovative data spatial programming model. The language also brings a fresh take for annotation and documentation, fostering readable and maintainable code.

As we delve into the details, bear in mind that though we will be elevating a 'pythonic' coding style to a 'jactastic' way of thinking, Jac's core principle is that of "python-complete" interoperability. Jac views the pythonic and the jactastic as a continuum that the language must support. A benefit to Jac users is that this also means they automatically inherit the rich ecosystem of Python libraries and frameworks, thus providing programmers with a diverse set of tools for various application domains. Jac's target bytecode is Python. All python libraries are Jac libraries, and a Jac object always maps to a Python object.

Lets jump in.

### Code Organization

In the Jac programming language, the fundamental organizational unit of code is the "module". Each Jac module is a coherent assembly of various elements in a source file. The complete set of these element include the following.

#### Module Elements

The comprehensive array of potential elements within a Jac module encompasses:

1. **Docstring**: This is a string literal that resides as the inaugural statement in a module. A docstring, the sole *mandatory* element, functions for documentation and clarifies the operations performed by the affiliated code.

1. **Import Directives**: These directives import other modules or elements from other modules, providing an avenue to adopt functionalities encapsulated in different modules. Import directives promote code reusability and modular design.

1. **Include Directives**: Occasionally, there's a necessity to directly integrate code into the prevailing namespace, as with definitions matching their declarations. To this end, `include` has been incorporated. Note, however, that with `import`, all entities—classes, functions, variables, and the like—from the imported module are housed under that module's namespace, effectively preventing collision.

1. **Function-style Abilities**: These are quintessential functions that replicate the standard Python `def` style function (augmented with a jactastic `can`), inclusive of input parameters and yielding a value.

1. **Data-spatial Abilities**: Akin to functions but with a unique data-spatial bend, these execute and yield values like functions, yet instead of accepting parameters, data-spatial abilities operate on the requisite data and apply a duck typing approach to their execution. They can be conceptualized as portable computation units dispatched to data elements, spawnable on any type, such as objects, dictionaries, lists, etc.

1. **Module Level Codeblocks**: Code situated at the module level is executable code not enclosed within a function or class. This code executes when the module is imported or initiated as a script, making it perfect for initializing module-level variables or executing setup tasks. A note of caution: its usage should be limited to enhance code readability and maintainability. Explicit specification of this with a module-level `with entry {}` directive is also enforced.

1. **Global Variables**: These can be declared and defined within a module, and are accessible throughout the module's scope. Yet, Jac's design philosophy mildly discourages heavy reliance on global variables, advocating for improved modularity, encapsulation, code readability, and codebase scalability. Overuse may lead to tightly coupled, less maintainable code.
    1. Note: Though Jac allows for the declaration of global variables, developers are encouraged to use this feature sparingly. Overreliance may result in hard-to-debug, complex code that lacks modularity, impacting the scalability of the codebase. Instead, the Jac language supports encapsulation and modular design via its architype and abilities system, promoting a cleaner, more maintainable, and scalable code.

1. **Test Definitions**: In alignment with software development best practices, Jac modules may include test definitions. These tests offer an automated method to verify the behavior of architypes, abilities, and other module components. They form an integral part of the development cycle, supporting continuous validation and confident refactoring of code. Test definitions can be structured as unit tests for individual components, integration tests for interoperability verification, and end-to-end tests to validate system-wide behavior.

1. **Architype Declarations**: An "architype" in the data-spatial programming paradigm is a type of class carrying unique semantics. It's a progression of the conventional "class" concept in Object-Oriented Programming. In Jac, an architype could manifest as traditional classes (Object Types), structures defining nodes in the data space (Node Types), instances of relationships between nodes (Edge Types), or agents traversing the graph data space (Walker Types), each possessing specific properties and relationships.

1. **Detached Definitions**: If an ability or architype is declared but not defined, their definitions can appear separately within the module file. This allows for a clear distinction between the declaration and implementation of architypes and abilities, offering flexibility in the organization of the module content and potentially enhancing code readability and beauty. It's also useful when the implementation of an architype or ability is large or complex, allowing for the separation of interface and implementation details within the module.


#### Architype elements

The term "architype" is a distinct concept introduced with the data spatial programming paradigm. It represents the notion that there can be several categories of classes, each carrying unique semantics. Every other OOP language we are aware of has a singular notion of a "class", so we use "architype" for brevity. In Jac, an architype can take one of the following forms:

1. **Object Types**: Traditional classes, as seen in Object-Oriented Programming (OOP), form the core primitive that Jac's other architypes build upon. Objects encapsulate data and the operations that can be performed on that data, but does not inherently harbor or encode relationships with other objects.

1. **Node Types**: Node types define the structure of individual nodes in the data space. They detail the properties and data that a node can hold. Node types are object that can inherently encode relationships and compatibility with other node types.

1. **Edge Types**: Edge types encode the semantics of an instance of relationship between nodes. They specify the nature of the relationship, including any constraints or properties associated with the particular connection.

1. **Walker Types**: Walker types encapsulate the logic for navigating the graph data space. They can be seen as agents that traverse nodes and edges to perform operations, gather information, and deploy information throughout nodes edges and objects.

(intrigued? hop to the red pill for more. scared? check out the blue pill. neither? read on.)



#### Minimal Code Example

The following code example shows all elements that form a Jac module.

```jac
--8<-- "examples/micro/module_structure.jac"
```

### Emphasizing the Separation of Declarations and Definitions

In the pursuit of more organized, scalable, and readable codebases, the Jac programming language revives the distinction between ability declarations and definitions. This approach is a deviation from Python, which do not explicitly separate method definitions from their declarations.

In Jac, a declaration refers to announcing the existence and signature of an ability to an object type, node type, edge type, or walker type. A declaration specifies the name and either data spatial event details, or method parameters and return details of an ability, but does not detail the actual implementation or behavior. On the other hand, a definition provides the complete description of the declared element, detailing how it operates or behaves. This can be specified within the same Jas module file, or in a separate module file.
#### Minimal Code Example
`main.jac`
```jac
--8<-- "examples/micro/decl_defs_split.jac"
```

`defs.jac`
```jac
--8<-- "examples/micro/decl_defs_imp.jac"
```

The benefits of this separation are manifold:

1. **Readability**: By separating the declaration from the definition, developers can easily understand what an element does just by looking at its signature, without getting lost in the details of its implementation.

2. **Organizational Clarity**: Declarations serve as an overview or table of contents for a module, making it easier to understand the module's structure and functionalities at a glance.

3. **Scalability**: The distinction allows for improved code organization in larger codebases. A module can contain declarations that are defined in different parts of the program, allowing for better distribution of code.

4. **Improved Debugging and Maintenance**: This approach makes debugging easier as it provides a clear distinction between interface and implementation. If a bug occurs, it is more straightforward to identify whether it's due to a faulty implementation or a misuse of the interface.

The reintroduction of this distinction in Jac reflects a philosophy of design clarity and software robustness. By encouraging developers to think about the interface of their code separate from its implementation, Jac promotes the development of clear, maintainable, and scalable software.

### Doc strings in Jac

Jac, compared to Python, offers a thoughtful approach to the implementation of docstrings, aiming to facilitate a cleaner and more helpful usage model for developers. The core philosophy of Jac is to ensure that docstrings are used in a way that truly benefits their intended purpose, which is to serve as an easily accessible documentation for modules, objects, or functions.

Python allows docstrings to appear virtually anywhere within the program. While this provides flexibility, it tends to blur the line between docstrings and comments, with developers often using them as a medium for writing comment. Docstrings should be strictly for documenting the purpose and usage of certain sections of the code. We have comments for... comments.

#### Jac's Approach to Docstrings

Unlike Python, Jac implements a strict yet sensible parser level rule on where docstrings should be placed within the code. The Jac language grammar asserts the position of docstrings are relegated to only placed where they are most beneficial.

In Jac, docstrings are only permitted in the following locations:

- At the start of modules as the first item
- In the beginning of object definitions as the first item
- In the beginning of code blocks that define functions, methods, and abilities as the first item

Indeed, these are the typical places you see docstrings in any good codebase, and these are the only locations that are recognized by most documentation generation tools for Python, yet!, we still see code with docstrings used willy nilly all over the place in various code bases :-P.

If a docstring appears in any arbitrary location that doesn't conform to the aforementioned rules, the Jac compiler will complain. This may seem strict but ensures a clean, concise, and effective usage of docstrings for their primary role: code documentation. Oh and the programs end up being more beautiful too!

Developers are still allowed the freedom to use any style of comments anywhere else in the code. This distinction emphasizes the point that docstrings and comments serve different roles: docstrings for code documentation, and comments for in-line explanations and code narrative.
