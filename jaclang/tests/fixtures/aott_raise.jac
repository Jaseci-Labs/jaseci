import:py from mtllm.llms.base, BaseLLM;

obj model:BaseLLM: {
    can __infer__(meaning_in: str, **kwargs: dict) {
        return "The calculated age is 145";
    }
}
glob llm = model();
glob  theresa: 'mother theresa':list[str, str] = ["Mother Theresa", "1910-08-26"];
obj 'Person'
Person {
    has name: 'Name' :str,
        dob: 'Date of Birth': str,
        age: 'Age': int = None;

    can 'Calculate the Age of a Person'
    calculate (cur_year: 'Current Year': int)
    -> 'Calculated Age' :int by llm(temperature=0.7, reason=True,incl_info=(self), excl_info=(self.age));
}
with entry{
    Einstein = Person(name="Einstein", dob="1879-03-14");
    age = Einstein.calculate(cur_year=2024);
    Einstein.age = age;
    print(Einstein.age);
}