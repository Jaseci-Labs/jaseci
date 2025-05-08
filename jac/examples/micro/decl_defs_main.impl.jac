"""Definitions of the walker and abilities."""

impl def travelor.say_hello {
    "Hello" |> print;  # |> is a pipe forward operator
}

# :w: and :c: are aliases for :walker: and :abilitiy:
impl def travelor.say_whatever(msg: str) -> None {
    msg |> print;
}