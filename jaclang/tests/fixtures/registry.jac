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
   INTROVERT: 'Person who is shy and reticent' = 9,
   EXTROVERT: 'Person who is outgoing and socially confident'
}

glob personality_examples: 'Personality Information of Famous People': dict[str, Personality|None] = {
    'Albert Einstein': Personality.INTROVERT,
    'Barack Obama': Personality.EXTROVERT
};

glob person_value : list[tuple[dict[str, Personality], int]] =(-90);

can foo() {
   person_value=22;
   can bar() {
       person_value=33;
   }
}
with entry {
    einstein_age: int = 75;
    einstein_age += 1;
    einstein = Person('Albert Einstein', einstein_age);
}
