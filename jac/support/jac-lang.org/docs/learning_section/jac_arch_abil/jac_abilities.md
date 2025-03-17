# Abilities in Jac

In Jac, **Abilities** define the actions that can perform. It is similar to **functions or methods** in other programming languages.

Abilities are defined using the `can` keyword.

---

### Define Abilities

Abilities are defined using the `can` keyword, followed by the ability name and its code block.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_ability.jac:1:3"
    ```

---

### Ability Parameters

Abilities can take parameters, just like functions.

**Code Example**
    ```jac linenums="5"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_ability.jac:5:7"
    ```

* This ability takes a name as input and prints a greeting message.

---

### Returning Values from Abilities

Abilities can return values using the `return` keyword. The retrun type should be specified before the body of the ability.

Example

- `-> int`
- `-> str`
- `-> float`

**Code Example**
    ```jac linenums="9"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_ability.jac:9:11"
    ```

* This ability takes two numbers, adds them, and returns the result.

---

### Abilities Inside Architypes

Abilities can be defined inside **architypes** (nodes, edges, objects, etc.).

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_abilities.jac"
    ```

---

### Static Abilities

Static abilities do not depend on instance data. They are defined using the `static` keyword.

**Code Example**
    ```jac linenums="13"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_ability.jac:13:17"
    ```

* This `square` ability does not require an instance of `MathUtils` and can be called directly.

---


### Overriding Abilities in Inheritance

If an `architype` inherits another, it can override its abilities.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_abil_override.jac"
    ```

* Here, `Dog` inherits `Animal` but overrides the `speak` ability with its own behavior.

---

### Abstract Abilities in Jac

In Jac, abilities define actions or behaviors within an architype. Some abilities can be **abstract**, meaning they provide a blueprint but do not contain actual implementations.

* It must be implemented in child architypes.
* It acts like an interface or contract for derived architypes.
* Declared using the `abs` keyword at the end of the definition.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_abil_abs.jac"
    ```

!!! warning
    Since `Shape` obj has an abstract ability, an instance cannot be initiated from `Shape`.

    So, This is not valid.
    ```
    with entry {
        s = Shape();
    }
    ```