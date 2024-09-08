import:py from mtllm.llms, Anthropic;

glob llm = Anthropic(model_name="claude-3-sonnet-20240229");

can 'Translate English Representation to the given language'
translate(input: 'English Representation': str, lang: 'Desired Language': str="French") -> 'Translation': str by llm();

with entry {
    print(translate("I am a student", "French"));
    print(
        translate("I am a student", "Language used in Somalia")
    );
}
