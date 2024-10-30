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

glob personality_examples: 'Personality Information of Famous People': dict[str, Personality | None] = {
    'Albert Einstein': Personality.INTROVERT,
    'Barack Obama': Personality.EXTROVERT
};

glob person_value: list[tuple[dict[str, Personality], int]] = (-90);

can 'GenAI ability'
genai_ability(x: 'Something': str) -> 'Something Else': str by llm();

can 'Normal ability'
normal_ability(x: 'Something': str) -> 'Something Else': str {
    y = 10;
    return x;
}

can foo() {
    person_value = 22;
    can bar() {
        person_value = 33;
    }
}
with entry {
    einstein_age: int = 75;
    einstein_age += 1;
    einstein = Person('Albert Einstein', einstein_age);
}

import from jaclang.runtimelib.machine { JacMachine }

with entry {
    registry = JacMachine.get().jac_program.sem_ir;

    print(len(registry.registry));
    print(len(list(registry.registry.items())[0][1]));
    print(list(registry.registry.items())[3][0].scope);
    (_, sem_info) = registry.lookup(name="normal_ability");
    print(len(sem_info.get_children(registry)));
}
