import:py from mtllm.llms, Anthropic;

glob llm = Anthropic(model_name="claude-3-sonnet-20240229");

enum 'Personality of the Person'
Personality {
    INTROVERT: 'Person who is shy and reticent' = "Introvert",
    EXTROVERT: 'Person who is outgoing and socially confident' = "Extrovert"
}

obj 'Person'
Person {
    has full_name: 'Fullname of the Person': str,
        yod: 'Year of Death': int,
        personality: 'Personality of the Person': Personality;
}

glob personality_examples: 'Personality Information of Famous People': dict[str, Personality] = {
    'Albert Einstein': Personality.INTROVERT,
    'Barack Obama': Personality.EXTROVERT
};

can 'Get Person Information use common knowledge'
get_person_info(name: 'Name of the Person': str) -> 'Person': Person by llm(
    reason=True,
    temperature=0.0,
    incl_info=(personality_examples)
);

with entry {
    person_obj = get_person_info('Martin Luther King Jr.');
    print(
        f"{person_obj.full_name} was a {person_obj.personality.value} person who died in {person_obj.yod}"
    );
}
