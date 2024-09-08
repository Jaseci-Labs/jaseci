glob x = "Jaclang ";

can foo() -> None {
    :g: x ;

    x = 'Jaclang is ';
    y = 'Awesome';
    can foo2() -> tuple[str, str] {
        :nl: y ;

        y = "Fantastic";
        return (x, y);
    }
    print(x, y);
    print(foo2());
}

with entry {
    foo();
}
