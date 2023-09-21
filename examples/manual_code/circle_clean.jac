"""
This module demonstrates a simple circle class and a function to calculate
the area of a circle in all of Jac's glory.
"""
import:py math;
include:jac circle_clean_impl;

enum ShapeType;
can calculate_area(radius: float) -> float;
can main_run;

"""Base class for a shape."""
object Shape {
    has shape_type: ShapeType;
    can area -> float abstract;
}

"""Circle class inherits from Shape."""
object Circle:Shape {
    has radius: float;
    can <init>;
    can area -> float;
}

# Radius of the demo circle
global RAD = 5, c = Circle(RAD);

"""Here we run the main program."""
with entry:__main__ { main_run(); }