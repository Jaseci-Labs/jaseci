"""Example for separation between declaration and definition."""

walker travelor {
    can say_hello with entry abs;  # data spatial ability declared
    can say_whatever(msg: str) -> None abs;  # traditional method declared

    # inline ability definition (python only supports this)
    can say_goodbye {
        "Goodbye" |> print;
    }
}