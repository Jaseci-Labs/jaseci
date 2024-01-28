from __future__ import annotations

x = "Jaclang "


def foo() -> None:
    global x
    x = "Jaclang is "
    y = "Awesome"

    def foo2() -> tuple[str, str]:
        nonlocal y
        y = "Fantastic"
        return (x, y)

    print(x, y)
    print(foo2())


foo()
