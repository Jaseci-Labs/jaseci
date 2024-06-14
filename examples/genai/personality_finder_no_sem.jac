import:py from jaclang.core.llms, Anthropic, Ollama, Groq;

# glob llm = Anthropic(model_name="claude-3-sonnet-20240229");
# glob llm = Groq();
glob llm = Ollama(model_name="phi3", verbose=True);


enum Personality {
   INTROVERT = "Introvert",
   EXTROVERT = "Extrovert"
}

obj Person {
    has full_name: str,
        year_died: int,
        personality: Personality;
}

# glob personality_examples: dict[str, Personality] = {
#     'Albert Einstein': Personality.INTROVERT,
#     'Barack Obama': Personality.EXTROVERT
# };

can get_person_info(name: str) -> Person
by llm(reason= True, temperature=0.0);

with entry {
    person_obj = get_person_info('Martin Luther King Jr.');
    print(f"{person_obj.full_name} was a {person_obj.personality.value} person who died in {person_obj.year_died}");
}