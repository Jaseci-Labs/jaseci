glob x = "Jaclang ";

def outer_func -> None {
    :g: x;

    x = 'Jaclang is ';
    y = 'Awesome';
    def inner_func -> tuple[str, str] {
        :nl: y;

        y = "Fantastic";
        return (x, y);
    }
    print(x, y);
    print(inner_func());
}

with entry {
    outer_func();
}
