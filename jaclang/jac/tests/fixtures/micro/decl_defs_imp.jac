:walker:travelor:ability:say_hello {
    "Hello" |> print;  # |> is a pipe forward operator
}

# :w: and :a: are aliases for :walker: and :abilitiy:
:w:travelor:a:say_whatever(msg: str) { 
    msg |> print;
}