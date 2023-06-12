"""Same functionality 3 white space styles."""

with entry { "hello" |> len |> print; }  # more concise

with entry {  # a bit more python like
    a = "hello" |> len;
    a |> print;
}

with entry {  # very pythonic
    a = "hello";
    b = len("hello");
    print(b); }