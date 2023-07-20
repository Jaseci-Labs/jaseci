"""Example of simple walker walking nodes."""

node item {
    has value: int;
}

walker creator {
    has count: int = 0;
    can create with <root>, item enter {
        <here> ++> spawn item;
        <self>.count += 1;
        if <self>.count < 10 {
            visit -->;
        }
    }
}

walker walk {
    has count: int = 0;
    can step with item enter {
        <here>.value = <self>.count;
        <self>.count += 1;
        visit --> else {
            "Done walking." |> print;
            disengage;
        }
        f"Value: {<here>.value}" |> print;
    }
}