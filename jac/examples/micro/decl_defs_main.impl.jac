"""Definitions of the walker and abilities."""

:walker:travelor:can:say_hello {
    "Hello" |> print;  # |> is a pipe forward operator
}

# :w: and :c: are aliases for :walker: and :abilitiy:
:w:travelor:c:say_whatever(msg: str) -> None {
    msg |> print;
}