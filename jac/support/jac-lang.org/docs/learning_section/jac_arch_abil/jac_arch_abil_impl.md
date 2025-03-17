Jac provides implementations (impls) to extend or define abilities and attributes separately from the original architype definition. This makes the code modular, organized, and easier to maintain.

### Impls for Architypes

Architypes store data and define structures, like objects in OOP. Instead of defining everything inside them, implementations allow modifications later.

**Code Example**
Declaration of the Architype

```jac linenums="1"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_impl.jac:1:1"
```

Implementation of the Architype
```jac linenums="2"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_impl.jac:3:7"
```

---

### Impls for Abilities

In Jac, abilities (can) can be declared separately from their implementations. This allows better modularity and organization of the code.

**Code Example**

Declaration of the Ability
```jac linenums="1"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_abil_impl.jac:1:1"
```

Implementation of the Ability

```jac linenums="2"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_abil_impl.jac:3:5"
```

---

### Impls for Abilities Inside Architypes

In Jac, abilities (`can`) inside architypes (like `walker`, `object`, `node`, etc.) can be **declared separately** from their implementations. This keeps the structure modular and improves clarity.

**Code Example**

Abilities can be **declared inside an architype** without defining their behavior.

```jac linenums="1"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_abil_impl.jac:1:3"
```

We can implement the ability **outside** the architype declaration.

```jac linenums="5"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_abil_impl.jac:5:7"
```