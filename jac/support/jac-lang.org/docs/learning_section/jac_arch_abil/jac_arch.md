---
title: Architypes and Abilities
---

### What are Architypes?
In Jac, **Architypes** define the fundamental building blocks of a program. They describe different types of entities that interact within the system.


### Types of Architypes

Architypes define different types of entities in Jac, used for both **object-oriented** and **graph-based programming.**

- **`class`** - A **standard class** used for object-oriented programming. It defines reusable structures with attributes and methods.

    ```jac
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_def.jac:2:2"
    ```

- **`obj`** - Similar to class, but represents **single-instance objects** rather than reusable templates.

    ```jac
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_def.jac:4:4"
    ```

!!! note
    We need `node`, `edge` and `walker` Architypes specially for **Data Spatial Programming concept** in Jac.


- **`node`** - Represents a **node** in a graph-based structure. Nodes store data and are connected using edge architypes.

    ```jac
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_def.jac:6:6"
    ```

- **`edge`** - Defines the **connection** between two `node` architypes. Edges store relationships between nodes.

    ```jac
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_def.jac:8:8"
    ```

- **`walker`** -  A special type of architype that **traverses** a graph, moving between `node` instances along `edge` connections. Walkers define behaviors for navigating structured data.

    ```jac
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_def.jac:10:10"
    ```


### Create an Architype

Let's start by creating a simple architype named Person. Architypes define entities in Jac and can later be extended with attributes and abilities.

The following example, `obj MyObject` contains ability. So, we'll explore it in **Arributes in Architypes** section.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_other.jac:6:8"
    ```


### Create Object

Now we can use the obj named MyClass to create the object.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_other.jac:10:13"
    ```

??? tip "Output"
    ```
    2
    ```