walker travelor {
    can say_hello with entry;  # data spatial ability declared
    can say_whatever(msg: str): None;  # traditional method declared

    # inline ability definition (python only supports this)
    can say_goodbye {
        "Goodbye" |> print;
    }
}