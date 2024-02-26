obj model {
    can __infer__(meaning_in: str, **kwargs: dict) {
        return meaning_in;
    }
}
glob llm = model();

can 'Summarize the Life of the Individual'
summarize(name: str) with llm(reason=True);

with entry {
    print(summarize('Albert Einstein'));
}