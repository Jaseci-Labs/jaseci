# Basic Syntax

##  No More Forced Indents with Jac

Jac loves Python's syntax but isn't a fan of the forced indentation for defining scopes. Jac introduces curly braces `{}` and semicolons `;` for statement terminators (similar to most other languages in existance).

In Python, indentation determines the beginning and end of blocks, which we observe being problematic in many places.
Jac retains Python's readability while eliminating issues associated with whitespace.

## Basic Statement

Every statement in Jac ends with a semicolon `;`.

```jac
print("Hello, Jac!");
```

## Variables

Variable declaration and assignment remain identical to Python though its not the line break that signifies the end of a statement, it's the semicolon.

```jac
x = 10;
y = 20;
print(x + y);
```

## Control Structures

Control structures in Jac are defined using curly braces `{}` and not indentation.

### If-else

```jac
if (x > y) {
    print("x is greater");
} else {
    print("y is greater");
}
```

And you can also do

```jac
if (x > y) { print("x is greater"); }
else { print("y is greater"); }
```

or

```jac
if (x > y) { print("x is greater"); } else { print("y is greater"); }
```

or even

```jac
if (x > y)
    {print("x is greater");}
else
    {print("y is greater");}
```

### Loops

For loops and while loops:

```jac
for i in range(5) {
    print(i);
}

count = 0;
while (count < 5) {
    print(count);
    count += 1;
}
```

## Functions

Function definitions utilize curly braces `{}` to enclose the function body.

```jac
can greet(name: str) {
    print(f"Hello, {name}!");
}

with entry { greet("Jac"); }
```

## Classes

Class definitions and methods also follow the curly brace convention.

```jac
object Rectangle {
    has width: float, height:float;

    can area(self) {
        return self.width * self.height;
    }
}

can start {
    rect = Rectangle(10, 5);
    print(rect.area());
}
```

## Exception Handling

Similar to Python, you can handle exceptions using `try`, `except`, `else`, and `finally`. However, in Jac, you'd surround these blocks with curly braces.

```jac
try {
    # Intentional error for demonstration
    result = 10 / 0;
} except ZeroDivisionError {
    print("Cannot divide by zero");
} else {
    print("Division successful");
} finally {
    print("This will execute no matter what");
}
```

## Migrating from Python

If you're transitioning from Python, remember the primary changes:

1. **Curly Braces `{}`**: Use them to define blocks of code.
2. **Semicolons `;`**: End each statement with them.

Jac provides this fresh approach for developers who appreciate Python's syntax but prefer braces and semicolons for defining scope.