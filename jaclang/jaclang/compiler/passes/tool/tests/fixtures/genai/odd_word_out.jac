import:py from mtllm.llms, Anthropic;

glob llm = Anthropic(model_name="claude-3-sonnet-20240229");

glob examples: 'Examples for Picking Odd Word out': list[dict] = [
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

can 'Pick only the Odd word out'
pick_odd_word_out_v1(options: 'Options to pick from': list[str]) -> 'RESULT': str by llm(reason=True, incl_info=(examples));
can 'Pick the Odd word out with reasoning'
pick_odd_word_out_v2(options: 'Options to pick from': list[str]) -> 'OPTIONS, REASONING & RESULT': dict[str, any] by llm(incl_info=(examples));

with entry {
    options = ["Bentley", "Ferrari", "Lamborghini", "Casio", "Toyota"];
    print(pick_odd_word_out_v1(options));
    print(pick_odd_word_out_v2(options));
}
