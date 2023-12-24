"""Example of simple walker walking nodes."""

node Item {
    has value: int = 1;
}

edge Checking {}

walker Creator {
    has count: int = 0;
    can create with `<root>|Item entry {
        print("on", id(<here>));
        print("edges before:", len(<here>._jac_.edges[_Jac.EdgeDir.OUT]));
        <here> ++> :> Item;
        print("edges after:", len(<here>._jac_.edges[_Jac.EdgeDir.OUT]));
        print([id(i) for i in <self>._jac_.next]);
        <self>.count += 1;
        if <self>.count < 10 {
            x=3;
            print([id(i) for i in <self>._jac_.next]);
            visit -->;
            print([id(i) for i in <self>._jac_.next]);
        }
        print("i was here", <self>.count);
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
    # :> Walk |> <root>;
}

with entry {
    |> test_run;
}