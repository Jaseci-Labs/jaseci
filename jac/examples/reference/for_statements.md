For statements in Jac provide powerful iteration mechanisms with multiple syntax variants to suit different looping scenarios. Jac supports both traditional iteration patterns and more expressive loop constructs that enhance readability and reduce common programming errors.

**For Loop Variants**

Jac provides three distinct for loop syntaxes:

1. **For-In loops**: Iterate over collections and iterables
2. **For-To-By loops**: Explicit counter-based iteration with clear termination conditions
3. **Async For loops**: Asynchronous iteration (when prefixed with `async`)

**For-In Loop Syntax**

For-in loops provide clean iteration over collections:
```jac
for variable in iterable {
    // loop body
}
```

**String Iteration**
```jac
for i in "ban" {
    print(i);  // Prints 'b', 'a', 'n'
}
```

This demonstrates:
- **Character iteration**: Strings are iterable character sequences
- **Automatic unpacking**: Each character assigned to the loop variable
- **Clear semantics**: Natural iteration over string contents

**Range Iteration**
```jac
for j in range(1, 3) {
    print(j);  // Prints 1, 2
}
```

Key aspects:
- **Range objects**: Generate sequences of numbers efficiently  
- **Boundary semantics**: End value is exclusive (like Python)
- **Memory efficiency**: Ranges generate values on demand

**Collection Iteration**
For-in loops work with all Jac collection types:
```jac
// List iteration
for item in [1, 2, 3, 4] {
    print(item);
}

// Dictionary iteration
for key in {"a": 1, "b": 2} {
    print(key);  // Iterates over keys
}

// Set iteration
for element in {1, 2, 3} {
    print(element);
}
```

**For-To-By Loop Syntax**

For-to-by loops provide explicit control over counter-based iteration:
```jac
for initialization to condition by increment {
    // loop body
}
```

**Example Usage**
```jac
for k=1 to k<3 by k+=1 {
    print(k);  // Prints 1, 2
}
```

**Components breakdown:**
- **Initialization**: `k=1` sets the starting value
- **Condition**: `k<3` specifies the continuation condition
- **Increment**: `k+=1` defines how the counter changes each iteration

**Advantages of For-To-By Syntax**

**Clarity**: Each component is explicitly labeled
```jac
for i=0 to i<10 by i+=2 {
    // Clear intent: start at 0, while i<10, increment by 2
}
```

**Flexibility**: Support for complex increment patterns
```jac
for count=100 to count>0 by count-=5 {
    // Countdown from 100 by 5s
}
```

**Error Prevention**: Explicit termination conditions reduce infinite loop risks
```jac
for index=0 to index<array.length by index+=1 {
    // Clear bounds checking
}
```

**Nested Loop Patterns**

The example demonstrates nested loops with different syntaxes:
```jac
for i in "ban" {          // Outer: for-in loop
    for j in range(1, 3) { // Middle: for-in with range
        for k=1 to k<3 by k+=1 { // Inner: for-to-by loop
            print(i, j, k);
        }
    }
}
```

**Expected output pattern:**
```
b 1 1
b 1 2
b 2 1
b 2 2
a 1 1
a 1 2
a 2 1
a 2 2
n 1 1
n 1 2
n 2 1
n 2 2
```

**Loop Variable Scope**

Loop variables are scoped to their respective loops:
- **Isolation**: Inner loop variables don't conflict with outer ones
- **Cleanup**: Variables automatically cleaned up when loops exit
- **Type inference**: Variable types inferred from iterables

**Advanced For-In Patterns**

**Enumeration**
```jac
for index, value in enumerate(collection) {
    print(index, value);
}
```

**Destructuring**
```jac
for key, value in dictionary.items() {
    print(key, value);
}
```

**Filtering**
```jac
for item in collection if item > threshold {
    process(item);
}
```

**Advanced For-To-By Patterns**

**Custom Increments**
```jac
for x=1.0 to x<=10.0 by x*=1.5 {
    // Exponential growth pattern
}
```

**Complex Conditions**
```jac
for i=0 to i<n and not found by i+=1 {
    if array[i] == target {
        found = true;
    }
}
```

**Multiple Variables**
```jac
for i=0, j=n-1 to i<j by i+=1, j-=1 {
    // Two-pointer technique
}
```

**Integration with Control Statements**

For loops work seamlessly with control statements:
```jac
for item in collection {
    if item.should_skip() {
        continue;  // Skip to next iteration
    }
    if item.is_terminal() {
        break;     // Exit loop entirely
    }
    process(item);
}
```

**Async For Loops**

For asynchronous iteration:
```jac
async for item in async_iterable {
    await process(item);
}
```

**Data Spatial Integration**

For loops integrate with data spatial constructs:
```jac
walker Iterator {
    can traverse with `node entry {
        for neighbor in [-->] {
            visit neighbor;
        }
    }
}
```

**Performance Considerations**

**For-In Optimization**
- **Iterator efficiency**: Optimized for collection traversal
- **Memory usage**: Minimal overhead for large collections
- **Type specialization**: Optimized paths for specific collection types

**For-To-By Optimization**
- **Counter efficiency**: Optimized arithmetic operations
- **Condition evaluation**: Efficient termination checking
- **Increment optimization**: Specialized operators for common patterns

**Common Patterns**

**Array Processing**
```jac
for i=0 to i<array.length by i+=1 {
    array[i] = transform(array[i]);
}
```

**Batch Processing**
```jac
for batch in chunked(data, batch_size=100) {
    process_batch(batch);
}
```

**Convergence Loops**
```jac
for iteration=0 to iteration<max_iterations and not converged by iteration+=1 {
    update_state();
    converged = check_convergence();
}
```

**Best Practices**

1. **Choose appropriate syntax**: Use for-in for collections, for-to-by for counters
2. **Clear variable names**: Use descriptive names for loop variables
3. **Avoid side effects**: Minimize modifications to collections during iteration
4. **Consider performance**: Choose efficient iteration patterns for large datasets
5. **Use control statements**: Leverage break and continue for complex logic

For statements in Jac provide flexible, expressive iteration capabilities that support both traditional programming patterns and modern language features. The multiple syntax variants enable developers to choose the most appropriate form for their specific use case, promoting code clarity and correctness while maintaining high performance.
