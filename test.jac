obj model {
    can __infer__(meaning_in: str, **kwargs: dict) {
        print(meaning_in);
    }
}
glob llm = model();

obj 'Person'
Person {
    has name: 'Name of the Person': str,
        age: 'Age of the Person': int;
}

enum 'Personality of the Person'
Personality {
   INTROVERT: 'Person who is shy and reticent',
   EXTROVERT: 'Person who is outgoing and socially confident';
}

can 'Get Personality of the Person'
get_personality (person: 'Person': Person) -> 'Personality of the Person': Personality by llm();

with entry {
    einstein = Person('Albert Einstein', 76);
    print(einstein.name);
    print(get_personality(einstein));
}
