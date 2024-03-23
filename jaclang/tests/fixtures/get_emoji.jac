obj model {
    can __infer__(meaning_in: str, **kwargs: dict) {
        print(meaning_in);
        return "{paris emoji}";
    }
}
glob llm = model();

glob emoji_examples: 'Examples of Text to Emoji': list[dict[str, str]] = [
    {
         "input": "I love football",
         "output": "{football emoji}"
    },
    {
        "input": "Lets eat pizza",
        "output": "{pizza emoji}"
    }

];
can 'Get Emoji Representation'
get_emoji(input: 'Input': str) -> 'Emoji Representation': str by llm(incl_info=(emoji_examples),excl_info=());

with entry {
    print(get_emoji('Lets move to paris'));
}


class 'Personality Index of a Person'
PersonalityIndex {
    can init(value: int) {
        self.index = value/10;
    }
}

enum 'Personality of the Person'
Personality {
   INTROVERT: 'Person who is shy and reticent',
   EXTROVERT: 'Person who is outgoing and socially confident'
}

glob personality_examples: 'Personality Information of Famous People': dict[str, Personality|None] = {
    'Albert Einstein': Personality.INTROVERT,
    'Barack Obama': Personality.EXTROVERT
};

obj 'Person'
Person {
    has name: 'Name of the Person': str,
        age: 'Age of the Person': int;
}

obj 'main object '
outer{
    obj 'inner object'
    inner{
        has in_var:'inner variable':int=9;
    can 'Get Personality of the Person'
get_personality (person: 'Person Object': list[Person]) -> 'Personality of the Person': dict[PersonalityIndex,Personality] by llm(reason=False, incl_info=(personality_examples,self.in_var), excl_info=(self.in_var));

    }
}

with entry{
    obj1=outer.inner(34);
    pp=Person('Albert Einstein', 76);
    print(obj1.get_personality(pp));
}
