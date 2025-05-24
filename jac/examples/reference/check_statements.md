### Check Statements
Check statements in Jac provide a built-in testing mechanism that integrates directly into the language syntax. They are primarily used within test blocks to verify that specific conditions hold true, forming the foundation of Jac's integrated testing framework.

**Basic Syntax**

The basic syntax for a check statement is:
```jac
check expression;
```

The `check` keyword evaluates the provided expression and verifies that it returns a truthy value. If the expression evaluates to false or a falsy value, the check fails and reports a test failure.

**Integration with Test Blocks**

Check statements are most commonly used within `test` blocks, which are Jac's language-level construct for organizing and running tests:

```jac
test test_name {
    check condition1;
    check condition2;
    // more checks...
}
```

**Types of Checks**

Check statements can verify various types of conditions:

**Equality and Comparison Checks**
- `check a == b;` - Verifies two values are equal
- `check a != b;` - Verifies two values are not equal  
- `check a > b;` - Verifies comparison relationships

**Function Result Checks**
- `check almostEqual(a, 6);` - Verifies function returns truthy value
- `check someFunction();` - Verifies function execution succeeds

**Membership and Containment Checks**
- `check "d" in "abc";` - Verifies membership relationships
- `check item in collection;` - Verifies containment

**Expression Evaluation Checks**
- `check a - b == 3;` - Verifies complex expressions evaluate correctly

**Testing Benefits**

The integration of check statements directly into the language provides several advantages:

- **Language-level support**: Testing is a first-class citizen in Jac
- **Simplified syntax**: No need to import testing frameworks
- **Clear semantics**: The `check` keyword makes test intentions explicit
- **Integrated reporting**: Failed checks are automatically reported by the language runtime

**Test Organization**

The provided code example demonstrates organizing multiple test cases using named test blocks (`test1`, `test2`, `test3`, `test4`), each containing specific check statements that verify different aspects of the global variables `a` and `b`.

Check statements make testing an integral part of Jac development, encouraging developers to write tests as they build their applications and ensuring code correctness through built-in verification mechanisms.
