"""Various samples to see code generated correctly"""

with entry {
    a=(5+10)*2;
    {"name": "value"} |> (len |> print |> dump) |> say;
}

with entry {
    a=(5+10)*2;
    {"name": "value"} |> (len |> print :> dump)  |> say;
}

with entry {
    len <| print  <| print  <| print <| {"name": "value"};
}

with entry {
    (*args, **kwargs) |> <s>.func;
    <s>.sig = func |> inspect.signature;
    |> <s>.registry.items;
}

with entry {
    with open("file.txt") as f, open("file2.txt") as f2 {}
}

enum Color {
    RED = 1,
    GREEN,
    BLUE = 3
}