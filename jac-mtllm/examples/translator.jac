import from mtllm.llms { OpenAI }

glob llm = OpenAI();

def translate(input: str, lang: str="French") -> str by llm();

with entry {
    print(translate("I am a student", "French"));
    print(
        translate("I am a student", "Language used in Somalia")
    );
}        
