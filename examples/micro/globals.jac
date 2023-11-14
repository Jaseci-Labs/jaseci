"""Globals are explicitly defined."""

glob age = 25, temperature = 98.6, name = "John Doe";
glob fruits = ["apple", "banana", "orange"];
glob person = {"name": "Alice", "age": 30, "city": "New York"};

can print_globs() -> None {
    :global:fruits,age; # :g: and :global: are equivalent
    age = 30;
    fruits = ["pear", "grape", "kiwi"];
    print(age, temperature, name);  # :g:<name> references global vs local
    fruits |> print;
    person |> print;
}