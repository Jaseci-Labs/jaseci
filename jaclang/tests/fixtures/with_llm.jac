obj model {
    can __infer__(meaning_in: str, **kwargs: dict) {
        print(kwargs);
        return "Albert Einstein was a German-born theoretical physicist "
        "who developed the theory of relativity, one of the two pillars "
        "of modern physics (alongside quantum mechanics). His work is also "
        "known for its influence on the philosophy of science. He is best known "
        "to the general public for his mass–energy equivalence formula E = mc^2, "
        "which has been dubbed 'the world's most famous equation'. He received "
        "the 1921 Nobel Prize in Physics 'for his services to theoretical physics, "
        "and especially for his discovery of the law of the photoelectric "
        "effect', a pivotal step in the development of quantum theory.";
    }
}
glob llm = model();

can 'Summarize the Life of the Individual'
summarize(name: 'Name of the Person': str, age: 'Age of the Person': int)
    -> 'Summary': str with llm(temperature=0.7, reason=True);

with entry {
    print(summarize('Albert Einstein',89));
}