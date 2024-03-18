obj model {
    can __infer__(meaning_in: str, **kwargs: dict) {
        print(meaning_in);
        print(kwargs);
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

enum 'Personality of the Person'
Personality {
   INTROVERT: 'Person who is shy and reticent' = 9,
   EXTROVERT: 'Person who is outgoing and socially confident'
}
can 'Get Emoji Representation'
get_emoji(input: 'Input': str) -> 'Emoji Representation': str by llm(incl_info=(emoji_examples),excl_info=());

with entry {
    print(get_emoji('Lets move to paris'));
}
obj 'Person'
Person {
    has name: 'Name of the Person': str,
        age: 'Age of the Person': int;
}

obj 'out sem '
outer{
    obj 'inner sem' inner{
        has vv:int=9;
    can 'Get Personality of the Person'
get_personality (person: 'Person Object': Person) -> 'Personality of the Person': Personality by llm(reason=True, incl_info=(personality_examples,self.vv));

    }
}
glob personality_examples: 'Personality Information of Famous People': dict[str, Personality|None] = {
    'Albert Einstein': Personality.INTROVERT,
    'Barack Obama': Personality.EXTROVERT
};


with entry{

    aa=outer.inner(34);

    print(aa.get_personality('Albert Einstein'));
}
