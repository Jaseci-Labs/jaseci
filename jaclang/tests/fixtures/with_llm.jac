obj model {
    can __infer__(meaning_in: str, **kwargs: dict) {
        return meaning_in;
    }
}
glob llm = model();

can 'do something' something(c: str) with llm(a="Hello", b="World");
with entry {
    print(something('test'));
}