obj model {
    can __infer__(meaning_in: str, **kwargs: dict) {
        print(meaning_in);
        print(kwargs);
        return "{paris emoji}";
    }
}
glob llm = model();


glob emoji_examples: 'Examples of Text to Emoji': list[dict[str, str]] = [
    {
         "input": "I love football",
         "output": "{football emoji}"
    },
    {
        "input": "Lets eat pizza",
        "output": "{pizza emoji}"
    }

];

can 'Get Emoji Representation'
get_emoji(input: 'Input': str) -> 'Emoji Representation': str by llm(incl_info=(emoji_examples),excl_info=());

with entry {
    print(get_emoji('Lets move to paris'));
}





