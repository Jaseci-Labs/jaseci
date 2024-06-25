import:py from mtllm.llms, Anthropic;

glob llm = Anthropic(model_name="claude-3-sonnet-20240229");

obj "A list of good dad jokes. A indicates the punchline"
JokeList {
    has jokes: 'Jokes with Punchlines': list[dict] = [
        {
            "joke": "How does a penguin build its house?",
            "punchline": "Igloos it together."
        },
        {
            "joke": "Which knight invented King Arthur's Round Table?",
            "punchline": "Sir Cumference."
        }
    ];

    can 'Generate a Joke with a Punchline'
    generate_joke_with_punchline -> 'Joke with Punchline': dict by llm(incl_info=(self.jokes), temperature=0.0);
    can generate {
        joke_punchline = self.generate_joke_with_punchline();
        self.jokes.append(joke_punchline);
    }
}

with entry {
    joke_gen = JokeList();
    for i in range(5) {
        joke_gen.generate();
    }
    print(joke_gen.jokes);
}
