# Separation of Declarations and Definitions in C++ vs Python

Jac has support to handle the concept of separating declarations and definitions differently than Python. This feature was introduced to the Jac language to drastically improve readability and maintainability of code bases (especially large ones!).  This tutorial will explain the differences and provide working code examples to illustrate them.

## Jac Declarations and Definitions

In Jac, you are able to separate declarations (which specifies what something *looks* like, i.e., the interface of a function) from definitions (which specifies what something *does*, i.e., the body of a function).

### Functions (Abilities)

In Jac:

1. **Declaration** - Specifies the function's name, return type, and its parameters. Does not provide the function body.
2. **Definition** - Provides the actual body of the function.

For instance:

```jac
--8<-- "examples/micro/decl_defs.jac:3:12"
```

### Classes and Methods

The same concept applies to classes and their member methods.

```jac
--8<-- "examples/micro/decl_defs.jac:14:25"
```

### Pythonic Combining of Decl/Defs

Jac also support the traditional pythonic style of combined declarations and definitions.

```jac
--8<-- "examples/micro/decl_defs.jac:28:42"
```

At first glance, one might conclude the pythonic style is more readable and easy to understand. However next we'll look at the implications of this design decision.
## Complex Real-World Example

Let’s look at a complex example using some code from Jac's compiler. Here we will take a look at the implementation of a pass of the Jac compiler that was written in Jac. This class is implemented across two files, one with the relevant declarations and the other with its definitions.

### Declarations in its Own File



First lets look at the declarations

**jaclang/jac/passes/purple/purple_pygen_pass.jac**
```jac
--8<-- "jaclang/jac/passes/purple/purple_pygen_pass.jac"
```

### Definitions in Separate File
**jaclang/jac/passes/purple/impl/purple_pygen_pass_impl.jac**
```jac
--8<-- "jaclang/jac/passes/purple/impl/purple_pygen_pass_impl.jac"
```

### Comparison with Python

Now lets take a look at a similar pass written in pure python. This is pep8 compliant python following a large number of recommended conventions. Experience its readability in seeing the interface of the class. (point: reading the interface and implementation together is not nice on the eyes.)
```python
--8<-- "jaclang/jac/passes/blue/decl_def_match_pass.py"
```

## Wrap-up

 Jac provides support for disconnected declarations and definitions as it enhances code readability and maintainability by providing a clear organizational structure to a codebase. Declarations, often placed in separate module files, serve as a concise interface, allowing developers to quickly grasp the functionality without delving into implementation details. Meanwhile, definitions encapsulate the actual logic, ensuring that changes to the logic do not necessitate modifications to the interface. This separation makes the code more modular, simplifying collaborations, facilitating code reviews, and allowing for more manageable compilation units in larger projects.