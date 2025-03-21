## Abilities Inside Architypes

Abilities can be defined inside **architypes** (nodes, edges, objects, etc.).

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architype/jac_arch_abilities.jac:1:23"
    ```

---

## Static Abilities

Static abilities do not depend on instance data. They are defined using the `static` keyword.

**Code Example**
    ```jac linenums="13"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_abilities/jac_ability.jac:13:17"
    ```

* This `square` ability does not require an instance of `MathUtils` and can be called directly.

---


## Overriding Abilities in Inheritance

If an `architype` inherits another, it can override its abilities.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architype/jac_arch_abilities.jac:27:31"
    ```

* Here, `Dog` inherits `Animal` but overrides the `speak` ability with its own behavior.

---

## Abstract Abilities in Jac

In Jac, abilities define actions or behaviors within an architype. Some abilities can be **abstract**, meaning they provide a blueprint but do not contain actual implementations.

* It must be implemented in child architypes.
* It acts like an interface or contract for derived architypes.
* Declared using the `abs` keyword at the end of the definition.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architype/jac_arch_abilities.jac:40:48"
    ```

!!! warning
    Since `Shape` obj has an abstract ability, an instance cannot be initiated from `Shape`.

    So, This is not valid.
    ```
    with entry {
        s = Shape();
    }
    ```