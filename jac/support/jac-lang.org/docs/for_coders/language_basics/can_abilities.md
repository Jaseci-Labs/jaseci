# Functions and Abilities

## `can` Abilities
In Jac's nomenclature, functions are refered to as *abilities*. While functions in python and abilities in jac are very similar, Python's `def` keyword is replaced with `can.`  Another key difference is that type hints are mandatory in Jac function signatures (for both parameters and return types), whereas they remain optional in Python. Any function that doesn't include its return signature (i.e., `-> TYPE`) is implicitly assumed to be `-> None`.

Unlike Python, Jac requires docstrings to appear before the function declaration. This design choice was made to improve readability, as placing function signatures closer to the implementation code enhances readability, especially when dealing with lengthy docstrings.

Let's look at some practical examples of Jac abilities in action:

```jac linenums="1"
"""Ability to calculate the area of a circle."""
can calculate_area(radius: float) -> float {
    return math.pi * radius * radius;
}

"""Processes a list of numbers and returns their sum.
Returns None if the list is empty.
"""
can sum_numbers(numbers: list[float]) -> float | None {
    if not numbers{
        return None;
    }
    return sum(numbers);
}
```

## Main Entry Point
In Jac, all executable code must be contained within structured blocks - there is no support for free-floating code (top-level code) as found in Python. The main entry point of a Jac program is defined using the `with entry` block. This block serves as the program's initialization and execution starting point, similar to Python's `if __name__ == "__main__"`: idiom but with mandatory usage. This design decision enforces a clear separation between declarations and executable code, leading to more maintainable and better-organized programs. However, when declaring multiple instances of ```with entry``` in one script, they will be executed one after the other, top to bottom.

Here's a clearer explanation with examples:

```jac linenums="1"
"""Calculates the area of a circle"""
can calculate_area(radius: float) -> float{
    return math.pi * radius * radius;
}

# Main entry point for the program
with entry{
    # Define constants
    RADIUS = 5.0;

    # Program execution
    print(f"Area of the circle: {calculate_area(RADIUS)}");
}
```