import:py from jaclang.core.llms, Anthropic;

glob llm = Anthropic(verbose=True, model_name="claude-3-sonnet-20240229");

obj JokeList {
    has jokes: list[dict] = [
        {
            "joke": "How does a penguin build its house?",
            "punchline": "Igloos it together."
        },
        {
            "joke": "Which knight invented King Arthur's Round Table?",
            "punchline": "Sir Cumference."
        }
    ];

    can generate_new_joke_with_punchline -> dict by llm(incl_info=(self.jokes), temperature=0.0); # ability name had to change from generate_joke_with_punchline to generate_new_joke_with_punchline

    can generate {
        joke_punchline = self.generate_new_joke_with_punchline();
        self.jokes.append(joke_punchline);
    }
}

with entry {
    joke_gen = JokeList();
    for i in range(5) {joke_gen.generate();}
    print(joke_gen.jokes);
}