Assert statements in Jac provide a mechanism for debugging and testing by allowing developers to verify that certain conditions hold true during program execution. When an assertion fails, it raises an `AssertionError` exception, which can be caught and handled like any other exception.

**Basic Assert Syntax**

The basic syntax for an assert statement is:
```jac
assert condition;
```

This will evaluate the condition, and if it is false or falsy, an `AssertionError` will be raised.

**Assert with Custom Message**

Jac also supports assert statements with custom error messages:
```jac
assert condition, "Custom error message";
```

When the assertion fails, the custom message will be included in the `AssertionError`, making debugging easier by providing context about what went wrong.

**Exception Handling**

Assert statements generate `AssertionError` exceptions when they fail, which can be caught using try-except blocks. This allows for graceful handling of assertion failures in production code or testing scenarios.

**Use Cases**

Assert statements are commonly used for:

- **Input validation**: Checking that function parameters meet expected conditions
- **Testing**: Verifying that code produces expected results
- **Debugging**: Ensuring that program state is as expected at specific points
- **Documentation**: Expressing assumptions about program behavior

The provided code example demonstrates a function `foo` that asserts its input parameter `value` must be positive. When called with a negative value (-5), the assertion fails and raises an `AssertionError` with the message "Value must be positive", which is then caught and handled in a try-except block.

Assert statements are an essential tool for writing robust and reliable Jac programs, providing early detection of invalid conditions and helping maintain program correctness.
