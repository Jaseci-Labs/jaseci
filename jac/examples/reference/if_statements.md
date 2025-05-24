If statements in Jac provide conditional execution control, allowing programs to make decisions based on boolean expressions. The if statement syntax supports the familiar if-elif-else pattern with code blocks, enabling complex conditional logic with clear, readable structure.

**Basic If Statement Syntax**

If statements follow this pattern from the grammar:
```jac
if condition {
    // code block
}
```

**Complete If-Elif-Else Structure**

The full conditional structure supports multiple branches:
```jac
if condition1 {
    // first condition block
} elif condition2 {
    // second condition block  
} else {
    // default block
}
```

**Example Implementation**

The provided example demonstrates a range-based conditional structure:
```jac
x = 15;
if 0 <= x <= 5 {
    print("Not Bad");
} elif 6 <= x <= 10 {
    print("Average");
} else {
    print("Good Enough");
}
```

**Key features demonstrated:**
- **Variable-based conditions**: Using variable `x` in conditional expressions
- **Chained comparisons**: `0 <= x <= 5` syntax for range checking
- **Sequential evaluation**: Conditions checked in order until one matches
- **Default handling**: `else` block executes when no previous conditions match

**Chained Comparison Operators**

Jac supports chained comparison operations, allowing elegant range checking:

**Range Checking**
```jac
if 0 <= value <= 100 {
    // value is in range [0, 100]
}
```

**Multiple Comparisons**
```jac
if a < b <= c < d {
    // Multiple relationships in single expression
}
```

**Supported Comparison Operators**
- **Equality**: `==`, `!=`
- **Ordering**: `<`, `<=`, `>`, `>=`
- **Identity**: `is`, `is not`
- **Membership**: `in`, `not in`

**Boolean Logic Integration**

If statements work with complex boolean expressions:

**Logical Operators**
```jac
if condition1 and condition2 {
    // Both conditions must be true
}

if condition1 or condition2 {
    // Either condition can be true
}

if not condition {
    // Condition must be false
}
```

**Mixed Expressions**
```jac
if (x > 0 and x < 100) or x == -1 {
    // Complex logical combinations
}
```

**Code Block Structure**

If statements require code blocks enclosed in curly braces:

**Single Statement Blocks**
```jac
if condition {
    single_statement();
}
```

**Multi-Statement Blocks**
```jac
if condition {
    first_statement();
    second_statement();
    result = calculation();
}
```

**Nested Blocks**
```jac
if outer_condition {
    if inner_condition {
        nested_logic();
    }
    outer_logic();
}
```

**Elif Chain Behavior**

Elif statements provide efficient multi-way branching:

**Sequential Evaluation**
```jac
if score >= 90 {
    grade = "A";
} elif score >= 80 {
    grade = "B";  // Only checked if score < 90
} elif score >= 70 {
    grade = "C";  // Only checked if score < 80
} else {
    grade = "F";  // Only if all conditions fail
}
```

**Early Termination**
- Once a condition matches, remaining elif/else blocks are skipped
- Ensures exactly one block executes
- Optimizes performance by avoiding unnecessary condition checks

**Expression Types in Conditions**

If statements accept various expression types:

**Boolean Expressions**
```jac
if is_valid and is_ready {
    proceed();
}
```

**Function Calls**
```jac
if validate_input(data) {
    process(data);
}
```

**Variable References**
```jac
if enabled {
    activate_feature();
}
```

**Complex Expressions**
```jac
if user.age >= minimum_age and user.has_permission("access") {
    grant_access();
}
```

**Integration with Data Spatial Features**

If statements work within data spatial contexts:

**Walker Abilities**
```jac
walker Processor {
    can process with `node entry {
        if here.is_processable {
            here.process();
            visit [-->];
        } else {
            disengage;
        }
    }
}
```

**Node Abilities**
```jac
node DataNode {
    can respond with Walker entry {
        if visitor.permission_level >= self.required_level {
            self.provide_data(visitor);
        }
    }
}
```

**Conditional Traversal**
```jac
if neighbor.is_accessible {
    visit neighbor;
} elif backup_path.exists {
    visit backup_path;
} else {
    disengage;
}
```

**Type-Safe Conditionals**

Jac's type system ensures conditional safety:

**Type Checking**
```jac
if isinstance(obj, SpecificType) {
    obj.specific_method();  // Type-safe access
}
```

**Null Safety**
```jac
if value is not None {
    process(value);  // Safe access after null check
}
```

**Performance Considerations**

If statements are optimized for efficiency:

**Short-Circuit Evaluation**
- `and` operations stop at first false condition
- `or` operations stop at first true condition
- Minimizes unnecessary computation

**Branch Prediction**
- Modern compilers optimize frequently taken branches
- Consistent condition patterns improve performance

**Common Patterns**

**Input Validation**
```jac
if input_data is None or len(input_data) == 0 {
    return error("Invalid input");
}
```

**Range Validation**
```jac
if not (0 <= index < len(array)) {
    throw IndexError("Index out of bounds");
}
```

**Configuration Checks**
```jac
if config.debug_mode {
    print("Debug: Processing item", item.id);
}
```

**Error Handling**
```jac
if operation.has_error() {
    log_error(operation.error);
    return failure_result;
} else {
    return operation.result;
}
```

**Best Practices**

1. **Clear Conditions**: Write readable boolean expressions
2. **Avoid Deep Nesting**: Use elif instead of nested if statements when possible
3. **Positive Logic**: Prefer positive conditions over negated ones when readable
4. **Consistent Style**: Use consistent indentation and formatting
5. **Early Returns**: Use early returns to reduce nesting in functions

**Comparison with Other Languages**

Jac's if statements provide:
- **Mandatory braces**: Always require `{}` for code blocks
- **Chained comparisons**: Natural mathematical notation support
- **Type safety**: Integration with Jac's type system
- **Data spatial integration**: Work seamlessly with walker and node abilities

If statements in Jac provide a familiar yet enhanced conditional execution mechanism that integrates smoothly with both traditional programming patterns and the language's innovative data spatial features. The support for chained comparisons and mandatory code blocks promotes both readability and safety in conditional logic.
