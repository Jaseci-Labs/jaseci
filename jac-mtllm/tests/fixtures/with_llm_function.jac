import from mtllm.llms { BaseLLM }

obj model(BaseLLM) {
    def init {
        super.__init__();
    }

    def __infer__(meaning_in: str, **kwargs: dict) {
        print(kwargs);
        print(meaning_in);
        return "[Output] Something";
    }
}

glob llm = model();

glob emoji_examples: 'Examples of Text to Emoji': list[dict[str, str]] = [
    {
        "input": "I love tp drink pina coladas",
        "output": "👤 ❤️ 🥤 🍍🥥"
    },
    {"input": "Mime Person", "output": "👤🤲🚷"}
];

can 'Get Emoji Representation'
get_emoji(input: 'Text Input': str) -> 'Emoji Representation': str by llm(
    temperature=0.7,
    incl_info=(emoji_examples),
    excl_info=()
);

with entry {
    print(get_emoji('Lets move to paris'));
}
