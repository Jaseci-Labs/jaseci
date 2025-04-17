## Introduction to Enumerations

What is an Enumeration?

- An `enum` is a special type in JacLang used to define a set of named constants.
- Used to represent finite sets of values, such as colors, roles, or states.
- Improves code readability and type safety.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_enum/jac_enum.jac:1:09"
    ```

## Enumeration with Values

Enums can be assigned **integer** or **string** values.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_enum/jac_enum.jac:11:18"
    ```

## Unique Enumeration Values (`@unique`)

Using `@unique` ensures that no two members of an enum have the same value.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_enum/jac_enum.jac:20:30"
    ```

## Protected Enumerations (`:protect`)

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_enum/jac_enum.jac:32:39"
    ```

## Enum with Methods (`can foo`)

Enums can have methods for additional functionality.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_enum/jac_enum.jac:41:52"
    ```

## Enum with `with entry` Block

Enums can have an entry block `(with entry)` that runs when they are first accessed.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_enum/jac_enum.jac:54:65"
    ```

## Nested Enumerations

Enums can be nested inside objects to define related constants.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_enum/jac_enum.jac:67:79"
    ```

## Enums Inside Nested Objects

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_enum/jac_enum.jac:81:105"
    ```

## Enum Comparison and Iteration

**1.Checking Equality**

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_enum/jac_enum.jac:107:113"
    ```

**2.Looping Through Enum Members**

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_enum/jac_enum.jac:115:119"
    ```
