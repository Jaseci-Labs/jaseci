import:py from jaclang.core.llms, Anthropic;

glob llm = Anthropic(verbose=True, model_name="claude-3-sonnet-20240229");



glob examples: list[dict] = [
    {
        "OPTIONS": ["skirt", "dress", "pen", "jacket"],
        "REASONING": "skirt is clothing, dress is clothing, pen is an object, jacket is clothing.",
        "RESULT": "pen"
    },
    {
        "OPTIONS": ["Spain", "France", "German", "England", "Singapore"],
        "REASONING": "Spain is a country, France is a country, German is a language, ...",
        "RESULT": "German"
    }
];

can pick_odd_word_out(options: list[str]) -> dict[str, any]
by llm(incl_info=(examples));

with entry {
    options = ["Bentley", "Ferrari", "Lamborghini", "Casio", "Toyota"];
    print(pick_odd_word_out(options));
}