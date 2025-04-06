Jac provides implementations (impls) to extend or define abilities and attributes separately from the original architype definition. This makes the code modular, organized, and easier to maintain.

## Impls for Architypes

Architypes store data and define structures, like objects in OOP. Instead of defining everything inside them, implementations allow modifications later.

**Code Example**
Declaration of the Architype

```jac linenums="1"
--8<-- "examples/learning_section/jac_architype/jac_arch_impl.jac:2:2"
```

Implementation of the Architype
```jac linenums="2"
--8<-- "examples/learning_section/jac_architype/jac_arch_impl.jac:4:8"
```

## Impls for Abilities Inside Architypes

In Jac, abilities (`can`) inside architypes (like `walker`, `object`, `node`, etc.) can be **declared separately** from their implementations. This keeps the structure modular and improves clarity.

**Code Example**

Abilities can be **declared inside an architype** without defining their behavior.

```jac linenums="1"
--8<-- "examples/learning_section/jac_architype/jac_arch_impl.jac:11:13"
```

We can implement the ability **outside** the architype declaration.

```jac linenums="5"
--8<-- "examples/learning_section/jac_architype/jac_arch_impl.jac:15:17"
```