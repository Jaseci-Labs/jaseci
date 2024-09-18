"""
This module demonstrates a simple circle class and a function to calculate
the area of a circle in all of Jac's glory.
"""

import:py math;

enum ShapeType;

can calculate_area(radius: float) -> float;
can main_run;

"""Base class for a shape."""
obj Shape {
    has shape_type: ShapeType;

    can area -> float abs;
}

"""Circle class inherits from Shape."""
obj Circle :Shape: {
    has radius: float;

    can init(radius: float);
    can area -> float;
}
# Radius of the demo circle

glob RAD = 5, c = Circle(radius=RAD);

"""Here we run the main program."""
with entry:__main__ {
    main_run();
}