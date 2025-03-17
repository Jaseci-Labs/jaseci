---
title: Architypes and Abilities
---

### What are Architypes?
In Jac, architypes define the fundamental building blocks of a program. They describe different types of entities that interact within the system.

!!! note
    We need Architypes for Spatial Programming concept in Jac.

---

### Types of Architypes
- **`class`**
- **`obj`**
- **`node`**
- **`edge`**
- **`walker`**
- **`object`**

Each architype is defined using a keyword (`class`, `obj`, `node`, `edge`, `walker`, `object`). Below is a simple example showing how they are declared.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_def.jac"
    ```

---

### Defining Architypes with Inheritance

Architypes can **inherit** properties and abilities from other architypes.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_inheritence.jac:1:8"
    ```

So, now the properties of `Animal` can be accessed through `Pet`.

**Code Example**
    ```jac linenums="9"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_inheritence.jac:10:14"
    ```

---

### String Identifiers in Architypes

Architypes can have an optional **string identifier** that describes them.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_other.jac:1:4"
    ```