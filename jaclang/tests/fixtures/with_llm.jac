obj model {
    can __infer__(**kwargs: dict) {
        return(kwargs);
    }
}
glob llm = model();

can something(c: str) -> Int with llm(a="Hello", b="World");
with entry {
    print(something('test'));
}