"""Example of simple walker walking nodes."""

node item {
    has value: int;
}

walker Creator {
    has count: int = 0;
    can create with <root>|:n:item enter {
        <here> ++> spawn :n:item;
        <self>.count += 1;
        if <self>.count < 10 {
            visit -->;
        }
    }
}

walker Walk {
    has count: int = 0;
    can skip_root with <root> enter { visit -->; }
    can step with :n:item enter {
        <here>.value = <self>.count;
        <self>.count += 1;
        visit --> else {
            f"Final Value: {<here>.value-1}" |> print;
            "Done walking." |> print;
            disengage;
        }
        f"Value: {<here>.value-1}" |> print;
    }
}

with enter {
    spawn :w:Creator |> <root>;
    spawn :w:Walk |> <root>;
}