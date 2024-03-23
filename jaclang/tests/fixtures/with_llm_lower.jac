obj model {
    can __infer__(meaning_in: str, **kwargs: dict) {
        return "[Output] Person(name='Oppenheimer', yod=1967, personality=Personality.INTROVERT)"
    }
}
glob llm = model();

enum 'Personality of the Person'
Personality {
   INTROVERT: 'Person who is shy and reticent',
   EXTROVERT: 'Person who is outgoing and socially confident'
}

obj 'Person'
Person {
    has name: 'Name of the Person': str,
        yod: 'Year of Death': int,
        personality: 'Personality of the Person': Personality;
}

glob personality_examples: 'Personality Information of Famous People': dict[str, Personality] = {
    'Albert Einstein': Personality.INTROVERT,
    'Barack Obama': Personality.EXTROVERT
};

can 'Get Person Information'
get_person_info(name: 'Name of the Person': str) -> 'Person' Person by llm(incl_info=(personality_examples))

with entry {
    print(get_person_info('Oppenheimer');)
}