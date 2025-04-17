# Jac Match-Case

## Introduction to Match-Case

What is Match-Case?

- match-case is a pattern-matching feature in JacLang that allows checking for different structures of data in a clean and readable way.
- Similar to switch-case in other languages but more powerful.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_match_case/jac_match_case.jac:1:11"
    ```

## Match by Value (`MatchValue`)

Match an exact value.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_match_case/jac_match_case.jac:13:20"
    ```

## Match Singleton (`MatchSingleton`)

Match **True**, **None**, or other singleton values.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_match_case/jac_match_case.jac:22:31"
    ```

## Match Lists (`MatchSequence`)

Match a specific sequence of elements.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_match_case/jac_match_case.jac:33:40"
    ```

## Match with Wildcards (`MatchStar`)

Use * to match unknown values in sequences.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_match_case/jac_match_case.jac:42:49"
    ```

## Match Dictionaries (`MatchMapping`)

Match key-value pairs in dictionaries.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_match_case/jac_match_case.jac:51:58"
    ```

## Match Classes (`MatchClass`)

Match objects using class patterns.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_match_case/jac_match_case.jac:60:71"
    ```

## Using as to Capture Values (`MatchAs`)

Extract matched values into variables.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_match_case/jac_match_case.jac:73:80"
    ```

## Match Multiple Patterns (`MatchOr`)

Use **|** to match multiple patterns.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_match_case/jac_match_case.jac:82:89"
    ```

## Default Case (_)

Use **_** to handle unmatched cases.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_match_case/jac_match_case.jac:91:98"
    ```
