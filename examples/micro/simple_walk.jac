"""Example of simple walker walking nodes."""

node item {
    has value: int;
}

walker creator {
    has count: int = 0;
    can create with <root>, :n:item enter {
        <here> ++> spawn :n:item;
        <self>.count += 1;
        if <self>.count < 10 {
            visit -->;
        }
    }
}

walker walk {
    has count: int = 0;
    can skip_root with <root> enter { visit -->; }
    can step with :n:item enter {
        <here>.value = <self>.count;
        <self>.count += 1;
        visit --> else {
            "Done walking." |> print;
            disengage;
        }
        f"Value: {<here>.value}" |> print;
    }
}

with enter {
    spawn :w:creator |> <root>;
    spawn :w:walk |> <root>;
}