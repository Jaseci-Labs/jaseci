"""Example for separation between declaration and definition.

A data-spatial object is shown in this example, however it applies
to all types of object classes.
"""

walker travelor {
    can say_hello with entry;  # data spatial ability declared
    def say_whatever(msg: str) -> None;  # traditional method declared

    # inline ability definition (python only supports this)
    def say_goodbye {
        "Goodbye" |> print;
    }
}