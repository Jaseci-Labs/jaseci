Abilities are similar to methods in traditional object-oriented programming; however, they have different syntax and semantics than standard functions. Jaclang uses `can` to declare abilities and uses `{}` to the ability body.
In Jaclang, abilities can be found in objects, classes, nodes, walkers, and edges. of a traditional function. Abilities can also exist in a standalone form, functioning similarly to standalone functions in other languages.

In the above example, there are a few uses of abilities within classes and objects. To find the uses of abilities inside the nodes, edges, and walkers, refer to the data spatial programming section in Jaclang.

Things to Note:

- **Abstract Abilities**: Use the `@abstractmethod` decorator to define abstract abilities similar to Python's abstract methods. Use `abs` as a placeholder for the abstract method, which is a shortened or implied version of the Python abstract method. For example, `can ability_name() -> return_type abs;`.

- **Static Abilities**: To declare static abilities, use the `static` keyword, for example: `static can static_ability() { // method body }`.

- **Class method declations**: Use the `@classmethod` decorator, i.e,

        ```
        @ classmethod
        can class_method(cls, arguments) {
            // method body
        }
        ```
- **Type hints**: Requred  type hints but has some differences in structure (e.g., `Dict[(str, str)]` instead of `Dict[str, str]`)
- **Custom decorators**: The custom decorator concept remains the same, but the syntax differs from Python.