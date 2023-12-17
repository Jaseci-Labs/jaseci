"""Example of simple walker walking nodes."""

node Item {
    has value: int = 1;
}

edge Checking {}

walker Creator {
    has count: int = 0;
    can create with `<root>|Item entry {
        <here> ++> :> Item;
        <self>.count += 1;
        if <self>.count < 10 {
            x=3;
            visit -->;
        }
        print("i was here");
    }
}

walker Walk {
    has count: int = 0;
    can skip_root with `<root> entry { x=3; visit -->; }
    can step with Item entry {
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

can test_run {
    :> Creator |> <root>;
    :> Walk |> <root>;
}

with entry {
    |> test_run;
}