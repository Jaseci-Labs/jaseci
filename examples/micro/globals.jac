"""Globals are explicitly defined."""

global age = 25, temperature = 98.6, name = "John Doe";
global fruits = ["apple", "banana", "orange"];
global person = {"name": "Alice", "age": 30, "city": "New York"};

can print_globs() -> None {
    :global:fruits,age; # :g: and :global: are equivalent
    age = 30;
    fruits = ["pear", "grape", "kiwi"];
    print(age, temperature, name);  # :g:<name> references global vs local
    fruits |> print;
    person |> print;
}