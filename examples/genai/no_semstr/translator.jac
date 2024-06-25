import:py from jaclang.core.llms, Anthropic;

glob llm = Anthropic(verbose=True, model_name="claude-3-sonnet-20240229");


can translate(input: str, lang: str = "French")
-> str by llm();

with entry {
    print(translate("I am a student", "French"));
    print(translate("I am a student", "Language used in Somalia"));
}