"""Various samples to see code generated correctly"""

with entry {
    a=(5+10)*2;
    {"name": "value"} |> (len |> print  |> dump)  |> say;
}

with entry {
    {"name": "value"} <| len <| print  <| print  <| print;
}

with entry {
    (*args, **kwargs) |> <s>.func;
    <s>.sig = func |> inspect.signature;
    |> <s>.registry.items;
}

with entry {
    with open("file.txt") as f, open("file2.txt") as f {}
}

enum Color {
    RED = 1,
    GREEN,
    BLUE = 3
}