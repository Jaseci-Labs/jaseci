"""Type hints aren't that much work."""

can foo(a: int, b: str): int {
    c = a + (b|>int);  # no type hint needed here
    return c;
}

object Bar {
    has a_list: list[int] = [1, 2, 3];
    has b_list: list[str] = ["5", "6", "7"];

    can entry(): None {
        for i in here.b_list {
            foo(5, i) |> print;
        }
    }
}