"""Various samples to see code generated correctly"""

with entry {
    a=(5+10)*2;
    {"name": "value"} |> (len |> print)  |> print  |> print;
}

with entry {
    {"name": "value"} <| len <| print  <| print  <| print;
}
