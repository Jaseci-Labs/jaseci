import:py from mtllm.llms, OpenAI;
import:py from mtllm.tools.wikipedia_utils, wikipedia_summary;

glob llm = OpenAI(verbose=True, model_name="gpt-4o-mini");

can get_answer(question: str) -> str by llm(method="ReAct", tools=[wikipedia_summary]);

with entry {
    question = "List the countries in the European Union";
    answer = get_answer(question);
    print("Question:", question);
    print("Answer:", answer);
}