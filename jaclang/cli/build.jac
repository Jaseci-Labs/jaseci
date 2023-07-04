"""
This is the implementation of the command line interface tool for the
Jac language. It's built with the Jac language via bootstraping and
represents the first such production Jac program.
"""

import:jac from cli, command_registry;

@command_registry.register
can foo(a: int = 4, b: str = "hello") -> str {
    return f"Foo result: {a}, {b}";
}

@command_registry.register
can bar(a: float = 4, b: int = 3, c: str = "hello") -> str {
    return f"Bar result: {a}, {b}, {c}";
}

