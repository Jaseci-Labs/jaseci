import contextlib
import os

from textwrap import dedent

@contextlib.contextmanager
def patch_file(filepath: str, new_content: str):
    """
    Context manager to temporarily replace file content for testing.
    Restores the original content after the block.
    """
    with open(filepath, "r") as f:
        original = f.read()
    try:
        with open(filepath, "w") as f:
            f.write(new_content)
        yield
    finally:
        with open(filepath, "w") as f:
            f.write(original)

def get_jac_file_path():
    """Return the absolute path to the sample Jac file used for testing."""
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../../examples/manual_code/circle.jac")
    )

def get_code(code: str) -> str:
    """Generate a sample Jac code snippet with optional test code injected."""
    jac_code = dedent(f'''
    """
    This module demonstrates a simple circle class and a function to calculate
    the area of a circle in all of Jac's glory.
    """

    import math;

    # Module-level global variable
    glob RAD = 5;

    """Function to calculate the area of a circle."""
    def calculate_area(radius: float) -> float {{
        return math.pi * radius * radius;
    }}

    #* (This is a multiline comment in Jac)
    Above we have the demonstration of a function to calculate the area of a circle.
    Below we have the demonstration of a class to calculate the area of a circle.
    *#

    """Enum for shape types"""
    enum ShapeType {{
        CIRCLE = "Circle",
        UNKNOWN = "Unknown"
    }}

    """Base class for a shape."""
    obj Shape {{
        has shape_type: ShapeType;

        """Abstract method to calculate the area of a shape."""
        def area -> float abs;
    }}

    """Circle class inherits from Shape."""
    obj Circle(Shape) {{
        def init(radius: float) {{
            super.init(ShapeType.CIRCLE);
            self.radius = radius;
        }}

        """Overridden method to calculate the area of the circle."""
        override def area -> float {{
            return math.pi * self.radius * self.radius;
        }}
    }}

    with entry {{
        c = Circle(RAD);
    }}

    # Global also works here

    with entry:__main__ {{
        # To run the program functionality
        print(
            f"Area of a circle with radius {{RAD}} using function: {{calculate_area(RAD)}}"
        );
        print(
            f"Area of a {{c.shape_type.value}} with radius {{RAD}} using class: {{c.area()}}"
        );
    }}

    # Unit Tests!
    glob expected_area = 78.53981633974483;
    {code}

    test calc_area {{
        check almostEqual(calculate_area(RAD), expected_area);
    }}

    test circle_area {{
        c = Circle(RAD);
        check almostEqual(c.area(), expected_area);
    }}

    test circle_type {{
        c = Circle(RAD);
        check c.shape_type == ShapeType.CIRCLE;
    }}
''')
    return jac_code