import:py from mtllm.llms {Gemini}

glob llm = Gemini(verbose=True);

can get_earth_circumference -> str by llm();

with entry {
    print(get_earth_circumference());
}