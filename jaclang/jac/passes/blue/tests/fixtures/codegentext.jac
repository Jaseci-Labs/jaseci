"""Various samples to see code generated correctly"""

with enter {
    a=(5+10)*2;
    {"name": "value"} |> (len |> print |> dump)  |> say;
}

with enter {
    a=(5+10)*2;
    {"name": "value"} |> (len |> print :> dump)  |> say;
}

with enter {
    {"name": "value"} <| len <| print  <| print  <| print;
}

with enter {
    (*args, **kwargs) |> <s>.func;
    <s>.sig = func |> inspect.signature;
    |> <s>.registry.items;
}

with enter {
    with open("file.txt") as f, open("file2.txt") as f {}
}

enum Color {
    RED = 1,
    GREEN,
    BLUE = 3
}