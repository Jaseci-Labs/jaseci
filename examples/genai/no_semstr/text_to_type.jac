import:py from jaclang.core.llms, Anthropic;

glob llm = Anthropic(verbose=True, model_name="claude-3-sonnet-20240229");

obj Employer {
    has employer_name: str,
        location: str;
}

obj Person {
    has name: str,
        age: int,
        employer: Employer,
        job: str;
}

with entry {
    info: str = "Kugesan is a 24 years old and works as an ML engineer at Jaseci Labs in Sri Lanka.";
    person = Person(by llm(incl_info=(info)));
    print(f"Person's name is {person.name} and works at {person.employer.employer_name} which is located in {person.employer.location}.");
}