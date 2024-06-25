import:py from mtllm.llms, BaseLLM;

obj model:BaseLLM: {
    can init {
        self.verbose = False;
        self.max_tries = 1;
    }
    can __infer__(meaning_in: str, **kwargs: dict) {
        print(meaning_in);
        return '[Reasoning] J. Robert Oppenheimer, also known as the "father of the atomic bomb," was a brilliant '
        'theoretical physicist and the director of the Manhattan Project during World War II. He played a crucial '
        'role in developing the first nuclear weapons. However, after witnessing the devastation caused by the '
        'atomic bombs dropped on Hiroshima and Nagasaki, he expressed deep regret and became an advocate for nuclear '
        'disarmament. While he was an exceptional scientist, he was also known for his introspective and philosophical '
        'nature, which suggests an introverted personality.\n'
        '[Output] Person(full_name="J. Robert Oppenheimer", yod=1967, personality=Personality.INTROVERT)';
    }
}
glob llm = model();

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
get_person_info(name: 'Name of the Person': str) -> 'Person': Person by llm(method="Reason");

with entry {
    person_obj = get_person_info('Oppenheimer');
    print(f"{person_obj.full_name} was a {person_obj.personality.value} person who died in {person_obj.yod}");
}