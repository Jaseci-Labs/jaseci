# Abilities in Jac

In Jac, **Abilities** define the actions that can perform. It is similar to **functions or methods** in other programming languages.

## Define Abilities

Abilities are defined using the `can` keyword, followed by the ability name and its code block.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_ability.jac:1:3"
    ```


## Ability Parameters

Abilities can take parameters, just like functions.

**Code Example**
    ```jac linenums="5"
    --8<-- "examples/learning_section/jac_ability.jac:5:7"
    ```

* This `say_hello_to` ability takes a `name` as input and prints a greeting message.


!!! note
    If the ability does not expect parameters, avoid using parentheses. For example,

    ```
    can foo() {}
    ```

    is unnecessary and should be written as

    ```
    can foo {}
    ```


## Calling Abilities in Jac

Once an ability is defined, it can be **called** just like functions in other languages. The way you call an ability depends on whether it has **parameters** or not.

### Calling Without Parameters

If an ability does not require parameters, you can simply call it by using its name followed by ().

**Code Example**
    ```jac linenums="5"
    --8<-- "examples/learning_section/jac_ability.jac:31:33"
    ```

- Since `say_hello` does not expect any input, it is called with empty parentheses `()`.


### Calling With Parameters

If an ability requires parameters, you must pass the appropriate values when calling it.

**Code Example**
    ```jac linenums="5"
    --8<-- "examples/learning_section/jac_ability.jac:35:37"
    ```

- The `say_hello_to` ability takes a `name` parameter, so we must pass a value when calling it.


## Returning Values from Abilities

Abilities can return values using the `return` keyword. The retrun type should be specified before the body of the ability.

Example

- `-> int`
- `-> str`
- `-> float`

**Code Example**
    ```jac linenums="9"
    --8<-- "examples/learning_section/jac_ability.jac:9:11"
    ```

* This ability takes two numbers, adds them, and returns the result.


## `*args` and `**kwargs` in Jac

In Jac, `*args` and `**kwargs` allow abilities to accept a **variable number of arguments**.


### Using `*args` (Positional Arguments)

- `*args` allows an ability to take multiple positional arguments.
- These arguments are received as a **list**.

**Code Example**
    ```jac linenums="9"
    --8<-- "examples/learning_section/jac_ability.jac:40:46"
    ```

- The `sum_all` ability accepts multiple numbers and adds them.


### Using `**kwargs` (Keyword Arguments)

- `**kwargs` allows an ability to accept multiple named arguments.
- These arguments are received as a **dictionary**.

**Code Example**
    ```jac linenums="9"
    --8<-- "examples/learning_section/jac_ability.jac:48:54"
    ```

- The `print_details` ability takes multiple named parameters and prints them.

## Access Tags for Abilities

In Jac, Access Tags control the visibility and accessibility of abilities. These tags determine whether an ability can be accessed from outside its defining scope.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_access_tag.jac:1:3"
    ```

The `pub` tag makes the ability accessible from anywhere. Similarly, Jac provides other access tags like `prot` and `priv`.

- We'll explore access tags in detail [here](./access_tags.md).


## String Identifiers in Abilities

Abilities can have an optional **string identifier** that describes them.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_ability.jac:19:21"
    ```


## Impls for Abilities

In Jac, abilities (can) can be declared separately from their implementations. This allows better modularity and organization of the code.

**Code Example**

Declaration of the Ability
```jac linenums="1"
--8<-- "examples/learning_section/jac_ability.jac:24:24"
```

Implementation of the Ability

```jac linenums="2"
--8<-- "examples/learning_section/jac_ability.jac:26:28"
```

## Recursion using Abilities

Recursion is a technique where a **function calls itself** to solve smaller subproblems. In Jac, abilities (`can`) can be recursive.

**Code Example 1: Factorial Calculation**
    ```jac linenums="9"
    --8<-- "examples/learning_section/jac_ability.jac:59:68"
    ```

**Code Example 2: Recursive Sum of a List**
    ```jac linenums="9"
    --8<-- "examples/learning_section/jac_ability.jac:71:80"
    ```