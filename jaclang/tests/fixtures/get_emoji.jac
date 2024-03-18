import:py openai;
import:py re;
obj model {
    can __infer__(meaning_in: str, **kwargs: dict) {
        print(meaning_in);
        print(kwargs);
        can llm(prompt:str){
            return openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                ).choices[0].message.content;

        }
        # response = llm(meaning_in);
        # return response;
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



enum 'Personality of the Person'
Personality {
   INTROVERT: 'Person who is shy and reticent' = 9,
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
get_personality (person: 'Person Object': Person) -> 'Personality of the Person': Personality by llm(reason=True, incl_info=(personality_examples,self.in_var));

    }
}

with entry{
    obj1=outer.inner(34);
    print(obj1.get_personality('Albert Einstein'));
}
