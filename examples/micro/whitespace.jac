"""Same functionality 3 white space styles."""

with enter { "hello" |> len |> print; }  # more concise

with enter {  # a bit more python like
    a = "hello" |> len;
    a |> print;
}

with enter {  # very pythonic
    a = "hello";
    b = len(a);
    print(b); }