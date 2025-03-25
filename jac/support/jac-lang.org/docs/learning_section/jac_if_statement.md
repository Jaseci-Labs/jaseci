Jac provides logical conditions similar to those found in other programming languages, allowing for decision-making using if statements. These conditions include:

   - **Equals (==)**: Checks if two values are equal.
   - **Not Equals (!=)**: Checks if two values are not equal.
   - **Less than (<)**: Checks if one value is smaller than another.
   - **Less than or equal to (<=)**: Checks if one value is smaller or equal to another.
   - **Greater than (>)**: Checks if one value is larger than another.
   - **Greater than or equal to (>=)**: Checks if one value is larger or equal to another.

if statements in Jac allow the program to execute different blocks of code based on these conditions. They are commonly used in decision-making and control flow.

## Basic If Statement
An **if statement** is written by using the if keyword.In Jac use curly-brackets to define scope in the code:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_if_stmt.jac:1:7"
    ```
In this example we use two variables, a and b, which are used as part of the if statement to test whether b is greater than a. As a is 5, and b is 20, we know that 20 is greater than 5, and so we print to screen that **"b is greater than a"**.

## Elif Statement
The **elif** keyword is Jac's way of saying if the previous conditions were not true, then try this condition:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_if_stmt.jac:9:17"
    ```

## Else Statement
The **else** keyword catches anything which isn't caught by the preceding conditions:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_if_stmt.jac:19:29"
    ```

In this example a is greater than b, so the first condition is not true, also the elif condition is not true, so we go to the else condition and print to screen that **"a is greater than b"**.

## And
The **and** keyword is a logical operator, and is used to combine conditional statements:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_if_stmt.jac:31:38"
    ```

## Or
The **Or** keyword is a logical operator, and is used to combine conditional statements:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_if_stmt.jac:40:47"
    ```

## Not
The **not** keyword is a logical operator, and is used to reverse the result of the conditional statement:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_if_stmt.jac:49:55"
    ```

## Nested If
You can have **if** statements inside **if** statements, this is called nested **if** statements.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_if_stmt.jac:57:67"
    ```
