"""A Docstring can be added the head of any module.

Any element in the module can also have a docstring.
If there is only one docstring before the first element,
it is assumed to be a module docstring.
"""

"""A docstring for add function"""
can add(a: int, b: int) -> int {
    return a + b;
}
# No docstring for subtract function

can subtract(a: int, b: int) -> int {
    return a - b;
}

with entry:__main__ {
    print(add(1, subtract(3, 1)));
}

glob x: int = 10;

enum Color {
    RED,
    GREEN,
    BLUE
}
obj Colour {
    has color: Color,
        point: int;

    can get_color -> Color;
}


:obj:Colour:can:get_color -> Color {
    return self.color;
}

obj red:Colour:{
    has base_color: Color = Color.RED,
        point: int = 10;
}

with entry:__main__ {
    r = red(color=Color.GREEN, point=20);
    print(r.get_color());
    
    red(color=Color.BLUE, point=30).
}